# Exemplo Prático: Criando um Agente de Análise de Sentimentos

Este exemplo mostra como usar o template para criar um agente especializado em análise de sentimentos de textos.

## 1. Gerando o Projeto

```bash
# Execute o cookiecutter
cookiecutter .

# Responda as perguntas:
project_name [My AI Agent]: Sentiment Analysis Agent
project_slug [sentiment-analysis-agent]:
agent_name [sentiment_analysis_agent]:
domain_name [sentimentanalysis]: sentiment
description [A specialized AI micro-agent for specific tasks]: An AI agent specialized in sentiment analysis of text content
author_name [Your Name]: João Silva
python_version [3.12]:
use_langsmith [yes]: yes
openai_model [gpt-4o-mini]: gpt-4o-mini
```

## 2. Configuração do Ambiente

```bash
# Entre no diretório do projeto
cd sentiment-analysis-agent

# Crie o arquivo .env baseado no ENV_VARS.md
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=sk-sua-chave-openai-aqui
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__sua-chave-langsmith-aqui
LANGCHAIN_PROJECT=sentiment-analysis-agent

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# FastAPI Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# SentimentAnalysisAgent Configuration
SENTIMENTANALYSISAGENT_MAX_RETRIES=3
SENTIMENTANALYSISAGENT_TIMEOUT=30
SENTIMENTANALYSISAGENT_ENABLE_REFLECTION=true
EOF

# Instale as dependências
uv sync
```

## 3. Personalizando o Agente

### 3.1. Customizar o Prompt Principal

Edite `app/application/agent/SentimentAnalysisAgent/node_functions/SentimentAnalysisAgent_node/node.py`:

```python
# Substitua o system_prompt por:
system_prompt = """You are a specialized AI agent for sentiment analysis.

Your task is to analyze the sentiment of the provided text content with the following capabilities:

1. **Sentiment Classification**: Classify the overall sentiment as:
   - POSITIVE (clearly positive emotions, satisfaction, joy, approval)
   - NEGATIVE (clearly negative emotions, dissatisfaction, anger, disapproval)
   - NEUTRAL (balanced, factual, or unclear emotional tone)

2. **Confidence Score**: Provide a confidence score (0.0 to 1.0) for your classification

3. **Key Indicators**: Identify the specific words or phrases that led to your classification

4. **Emotional Nuances**: Detect specific emotions like:
   - Joy, excitement, satisfaction (positive)
   - Anger, frustration, sadness, fear (negative)
   - Curiosity, confusion, indifference (neutral)

5. **Context Awareness**: Consider context, sarcasm, and implied meanings

Format your response as:
SENTIMENT: [POSITIVE/NEGATIVE/NEUTRAL]
CONFIDENCE: [0.0-1.0]
KEY_INDICATORS: [specific words/phrases]
EMOTIONS: [detected emotions]
ANALYSIS: [detailed explanation]"""

# E o human_prompt por:
human_prompt = f"""Please analyze the sentiment of the following text:

Text: {content}

Metadata: {metadata}

Provide a comprehensive sentiment analysis following the specified format."""
```

### 3.2. Customizar o Prompt de Reflexão

Edite `app/application/agent/SentimentAnalysisAgent/node_functions/reflect_node/node.py`:

```python
# Substitua o system_prompt por:
system_prompt = """You are a reflection agent that evaluates sentiment analysis results.

Your task is to:
1. Verify the accuracy of the sentiment classification
2. Check if the confidence score is appropriate
3. Validate that key indicators support the classification
4. Assess if emotional nuances were properly detected
5. Identify potential misinterpretations or biases

Be especially careful about:
- Sarcasm and irony detection
- Context-dependent sentiment
- Mixed emotions in the same text
- Cultural or domain-specific expressions

Provide feedback on accuracy and suggest improvements if needed."""
```

## 4. Testando o Agente

### 4.1. Executar o Servidor

```bash
# Execute o servidor
uv run uvicorn main:app --reload

# O servidor estará disponível em http://localhost:8000
# Documentação automática em http://localhost:8000/docs
```

### 4.2. Testes com Diferentes Tipos de Texto

#### Texto Positivo

```bash
curl -X POST http://localhost:8000/sentiment/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I absolutely love this new product! It exceeded all my expectations and made my life so much easier. Highly recommended!",
    "metadata": {"source": "product_review", "category": "technology"},
    "options": {"enable_reflection": false}
  }'
```

#### Texto Negativo

```bash
curl -X POST http://localhost:8000/sentiment/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This service is terrible. I waited for hours and nobody helped me. Completely disappointed and frustrated.",
    "metadata": {"source": "customer_feedback", "category": "service"},
    "options": {"enable_reflection": false}
  }'
```

#### Texto com Sarcasmo (Teste Complexo)

```bash
curl -X POST http://localhost:8000/sentiment/process-with-reflection \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Oh great, another meeting that could have been an email. Just what I needed to make my day perfect.",
    "metadata": {"source": "workplace_comment", "category": "sarcasm"},
    "options": {"enable_reflection": true}
  }'
```

#### Texto Neutro/Informativo

```bash
curl -X POST http://localhost:8000/sentiment/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The company reported quarterly earnings of $2.3 million, which represents a 5% increase compared to the same period last year.",
    "metadata": {"source": "financial_news", "category": "earnings"},
    "options": {"enable_reflection": false}
  }'
```

## 5. Exemplo de Resposta

O agente retornará algo como:

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "result": "SENTIMENT: POSITIVE\nCONFIDENCE: 0.95\nKEY_INDICATORS: ['absolutely love', 'exceeded all my expectations', 'made my life so much easier', 'Highly recommended']\nEMOTIONS: [joy, satisfaction, enthusiasm]\nANALYSIS: The text expresses strong positive sentiment through multiple positive indicators. The use of 'absolutely love' and 'exceeded expectations' shows high satisfaction. The recommendation at the end reinforces the positive sentiment.",
  "confidence_score": 0.95,
  "metadata": {
    "steps_completed": ["main_processing"],
    "reflection_enabled": false
  },
  "execution_time": 2.34,
  "tokens_used": 150,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:02Z"
}
```

## 6. Integrando com Kestra

### Exemplo de Flow no Kestra

```yaml
id: sentiment-analysis-flow
namespace: ai.agents

inputs:
  - id: text_content
    type: STRING
    required: true
  - id: source
    type: STRING
    defaults: "kestra"

tasks:
  - id: analyze-sentiment
    type: io.kestra.plugin.core.http.Request
    uri: http://sentiment-analysis-agent:8000/sentiment/process-with-reflection
    method: POST
    headers:
      Content-Type: "application/json"
    body: |
      {
        "content": "{{ inputs.text_content }}",
        "metadata": {
          "source": "{{ inputs.source }}",
          "flow_id": "{{ flow.id }}",
          "execution_id": "{{ execution.id }}"
        },
        "options": {
          "enable_reflection": true
        }
      }

  - id: process-result
    type: io.kestra.plugin.core.log.Log
    message: |
      Sentiment Analysis Complete:
      - Sentiment: {{ outputs['analyze-sentiment'].body.result }}
      - Confidence: {{ outputs['analyze-sentiment'].body.confidence_score }}
      - Execution Time: {{ outputs['analyze-sentiment'].body.execution_time }}s
```

## 7. Deploy em Produção

### Docker

```bash
# Build da imagem
docker build -t sentiment-analysis-agent .

# Execute o container
docker run -d \
  --name sentiment-agent \
  -p 8000:8000 \
  --env-file .env \
  sentiment-analysis-agent
```

### Docker Compose

```bash
# Execute com docker-compose
docker-compose up -d
```

### Kubernetes (exemplo básico)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-analysis-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-analysis-agent
  template:
    metadata:
      labels:
        app: sentiment-analysis-agent
    spec:
      containers:
        - name: agent
          image: sentiment-analysis-agent:latest
          ports:
            - containerPort: 8000
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: openai-secret
                  key: api-key
---
apiVersion: v1
kind: Service
metadata:
  name: sentiment-analysis-service
spec:
  selector:
    app: sentiment-analysis-agent
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

## 8. Monitoramento e Observabilidade

### Métricas Importantes

- Taxa de sucesso/erro das análises
- Tempo médio de processamento
- Distribuição de sentimentos detectados
- Uso de tokens OpenAI
- Scores de confiança médios

### Dashboard Example (Grafana)

```json
{
  "dashboard": {
    "title": "Sentiment Analysis Agent",
    "panels": [
      {
        "title": "Análises por Hora",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(sentiment_analyses_total[1h])"
          }
        ]
      },
      {
        "title": "Distribuição de Sentimentos",
        "type": "pie",
        "targets": [
          {
            "expr": "sentiment_positive_total",
            "legendFormat": "Positive"
          },
          {
            "expr": "sentiment_negative_total",
            "legendFormat": "Negative"
          },
          {
            "expr": "sentiment_neutral_total",
            "legendFormat": "Neutral"
          }
        ]
      }
    ]
  }
}
```

## 9. Próximos Passos

1. **Adicionar validação de entrada** mais robusta
2. **Implementar cache** para análises similares
3. **Adicionar suporte a múltiplos idiomas**
4. **Criar testes unitários** específicos para sentiment analysis
5. **Implementar rate limiting** para produção
6. **Adicionar métricas customizadas** com Prometheus
7. **Implementar fallback** para quando a API OpenAI não estiver disponível

Este exemplo mostra como o template pode ser rapidamente adaptado para casos de uso específicos, mantendo toda a estrutura robusta de Clean Architecture, LangGraph e integração com Kestra.
