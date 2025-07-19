"""
Reflection node for {{ cookiecutter.agent_name }}.
"""

import time
from datetime import datetime
from typing import Dict, Any

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from app.domain.state.{{cookiecutter.agent_name}}_state import AgentState, update_state_step
from app.infrastructure.llm.llm_factory import LLMFactory

logger = structlog.get_logger()


async def reflection_node(state: AgentState) -> Dict[str, Any]:
    """Reflection node for {{ cookiecutter.agent_name }}.
    
    This node reflects on the processing result and provides feedback.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state dictionary
    """
    logger.info("Executing reflection node")
    
    start_time = time.time()
    
    try:
        # Update state
        state = update_state_step(state, "reflection")
        
        # Get current result and original content
        result = state.get("result")
        content = state["input_content"]
        metadata = state["input_metadata"]
        
        if not result:
            logger.warning("No result to reflect on")
            return {
                "reflection_notes": "No result available for reflection",
                "confidence_score": 0.0,
                "current_step": "reflection",
                "last_updated_at": datetime.utcnow()
            }
        
        # Create LLM instance
        llm = LLMFactory.create_default_llm()
        parser = StrOutputParser()
        
        # Create reflection chain
        reflection_chain = llm | parser
        
        # Create reflection prompts
        system_prompt = """You are a reflection agent that evaluates the quality of {{ cookiecutter.domain_name }} processing results.

Your task is to:
1. Critically analyze the provided result
2. Assess its accuracy, completeness, and relevance
3. Identify areas for improvement
4. Provide a confidence score from 0.0 to 1.0
5. Suggest specific improvements if needed

Be objective and constructive in your feedback."""

        human_prompt = f"""Please reflect on this {{ cookiecutter.domain_name }} processing result:

ORIGINAL CONTENT:
{content}

PROCESSING RESULT:
{result}

METADATA:
{metadata}

Provide a detailed reflection covering:
1. Quality assessment (accuracy, completeness, relevance)
2. Confidence score (0.0 to 1.0) with justification
3. Specific areas for improvement if any
4. Overall recommendation (accept, improve, or retry)

Format your response as:
QUALITY: [assessment]
CONFIDENCE: [score]
IMPROVEMENTS: [specific suggestions]
RECOMMENDATION: [accept/improve/retry]"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Process reflection
        logger.info("Performing reflection on result")
        
        reflection_result = await reflection_chain.ainvoke(messages)
        
        execution_time = time.time() - start_time
        
        # Parse reflection result
        reflection_data = parse_reflection_result(reflection_result)
        
        # Estimate tokens used
        tokens_used = estimate_reflection_tokens(content, result, reflection_result)
        
        logger.info(
            "Reflection completed",
            execution_time=execution_time,
            confidence_score=reflection_data["confidence_score"],
            recommendation=reflection_data["recommendation"],
            tokens_used=tokens_used
        )
        
        # Update state with reflection
        return {
            "reflection_notes": reflection_result,
            "confidence_score": reflection_data["confidence_score"],
            "improvement_suggestions": reflection_data["improvements"],
            "current_step": "reflection",
            "last_updated_at": datetime.utcnow(),
            "execution_metadata": {
                **state.get("execution_metadata", {}),
                "reflection": {
                    "execution_time": execution_time,
                    "tokens_used": tokens_used,
                    "recommendation": reflection_data["recommendation"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            },
            "tokens_used": state.get("tokens_used", 0) + tokens_used
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        logger.error(
            "Reflection node failed",
            error=str(e),
            execution_time=execution_time,
            exc_info=True
        )
        
        return {
            "error_messages": [f"Reflection failed: {str(e)}"],
            "reflection_notes": f"Reflection failed due to error: {str(e)}",
            "current_step": "reflection",
            "last_updated_at": datetime.utcnow()
        }


def parse_reflection_result(reflection_text: str) -> Dict[str, Any]:
    """Parse reflection result to extract structured data.
    
    Args:
        reflection_text: Raw reflection text
        
    Returns:
        Parsed reflection data
    """
    result = {
        "confidence_score": 0.7,  # Default
        "improvements": [],
        "recommendation": "accept"
    }
    
    lines = reflection_text.lower().split('\n')
    
    for line in lines:
        if line.startswith('confidence:'):
            try:
                # Extract confidence score
                score_text = line.split('confidence:')[1].strip()
                score = float(score_text.split()[0])
                result["confidence_score"] = max(0.0, min(1.0, score))
            except (ValueError, IndexError):
                pass
                
        elif line.startswith('improvements:'):
            # Extract improvements
            improvements_text = line.split('improvements:')[1].strip()
            if improvements_text and improvements_text != "none":
                result["improvements"] = [improvements_text]
                
        elif line.startswith('recommendation:'):
            # Extract recommendation
            rec = line.split('recommendation:')[1].strip()
            if rec in ["accept", "improve", "retry"]:
                result["recommendation"] = rec
    
    return result


def estimate_reflection_tokens(content: str, result: str, reflection: str) -> int:
    """Estimate tokens used in reflection.
    
    Args:
        content: Original content
        result: Processing result
        reflection: Reflection result
        
    Returns:
        Estimated token count
    """
    # Rough estimation: ~4 characters per token
    content_tokens = len(content) // 4
    result_tokens = len(result) // 4
    reflection_tokens = len(reflection) // 4
    
    # Add system prompt overhead
    system_overhead = 150
    
    return content_tokens + result_tokens + reflection_tokens + system_overhead 