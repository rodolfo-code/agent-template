"""
Main processing node for {{ cookiecutter.agent_name }}.
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


async def main_processing_node(state: AgentState) -> Dict[str, Any]:
    """Main processing node for {{ cookiecutter.agent_name }}.
    
    This node performs the core processing task for the agent.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state dictionary
    """
    logger.info("Executing main processing node")
    
    start_time = time.time()
    
    try:
        # Update state
        state = update_state_step(state, "main_processing")
        
        # Get content and metadata
        content = state["input_content"]
        metadata = state["input_metadata"]
        
        # Create LLM instance
        llm = LLMFactory.create_default_llm()
        parser = StrOutputParser()
        
        # Create processing chain
        processing_chain = llm | parser
        
        # Create prompts
        system_prompt = """You are a specialized AI agent for {{ cookiecutter.domain_name }} processing.

Your task is to analyze and process the provided content according to the following requirements:

1. Carefully analyze the input content
2. Apply domain-specific knowledge for {{ cookiecutter.domain_name }}
3. Provide a comprehensive and accurate result
4. Ensure the output is well-structured and informative

Be thorough, accurate, and provide actionable insights where applicable."""

        human_prompt = f"""Please process the following {{ cookiecutter.domain_name }} content:

Content: {content}

Metadata: {metadata}

Provide a detailed analysis and processing result."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Process with LLM
        logger.info("Processing content with LLM", content_length=len(content))
        
        result = await processing_chain.ainvoke(messages)
        
        execution_time = time.time() - start_time
        
        # Calculate confidence score (simple heuristic)
        confidence_score = calculate_confidence_score(result, content)
        
        # Estimate tokens used (rough approximation)
        tokens_used = estimate_tokens_used(content, result)
        
        logger.info(
            "Main processing completed",
            execution_time=execution_time,
            result_length=len(result) if result else 0,
            confidence_score=confidence_score,
            tokens_used=tokens_used
        )
        
        # Update state with results
        return {
            "result": result,
            "confidence_score": confidence_score,
            "execution_time": execution_time,
            "tokens_used": tokens_used,
            "current_step": "main_processing",
            "last_updated_at": datetime.utcnow(),
            "intermediate_results": [result],
            "execution_metadata": {
                "node": "main_processing",
                "execution_time": execution_time,
                "tokens_used": tokens_used,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        logger.error(
            "Main processing node failed",
            error=str(e),
            execution_time=execution_time,
            exc_info=True
        )
        
        return {
            "error_messages": [f"Main processing failed: {str(e)}"],
            "execution_time": execution_time,
            "current_step": "main_processing",
            "last_updated_at": datetime.utcnow()
        }


def calculate_confidence_score(result: str, input_content: str) -> float:
    """Calculate confidence score for the processing result.
    
    Args:
        result: Processing result
        input_content: Original input content
        
    Returns:
        Confidence score between 0 and 1
    """
    if not result or not result.strip():
        return 0.0
    
    # Simple heuristics for confidence calculation
    score = 0.5  # Base score
    
    # Length-based confidence
    if len(result) > 50:
        score += 0.2
    
    # Content relevance (simple keyword matching)
    input_words = set(input_content.lower().split())
    result_words = set(result.lower().split())
    
    if input_words and result_words:
        overlap = len(input_words.intersection(result_words))
        relevance = overlap / len(input_words) if input_words else 0
        score += relevance * 0.3
    
    # Structure indicators
    if any(indicator in result.lower() for indicator in 
           ["analysis:", "conclusion:", "summary:", "result:"]):
        score += 0.1
    
    return min(score, 1.0)


def estimate_tokens_used(input_content: str, result: str) -> int:
    """Estimate tokens used in processing.
    
    Args:
        input_content: Input content
        result: Processing result
        
    Returns:
        Estimated token count
    """
    # Rough estimation: ~4 characters per token
    input_tokens = len(input_content) // 4
    output_tokens = len(result) // 4 if result else 0
    
    # Add system prompt overhead
    system_overhead = 100
    
    return input_tokens + output_tokens + system_overhead 