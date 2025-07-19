# Como Usar o Template Cookiecutter de Micro-Agentes

Este guia mostra como testar e usar o template Cookiecutter para criar micro-agentes Python especializados.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

```bash
# Python 3.12+
python --version

# Cookiecutter
pip install cookiecutter

# uv (gerenciador de pacotes)
pip install uv
```

## 1. Testando o Template Localmente

### Passo 1: Clone ou use o template local

```bash
# Se estiver testando localmente (no diretório atual)
cookiecutter .

# Ou se o template estiver em um repositório
# cookiecutter https://github.com/seu-usuario/agent-template
```

### Passo 2: Configure o novo projeto

O Cookiecutter solicitará as seguintes informações:

```
project_name [My AI Agent]: News Summarization Agent
project_slug [news-summarization-agent]:
agent_name [NewsSummarizationAgent]:
domain_name [newssummarization]: news
description [A specialized AI micro-agent for specific tasks]: An AI agent specialized in summarizing news articles
author_name [Your Name]: Seu Nome
author_email [your.email@example.com]: seu.email@example.com
python_version [3.12]:
use_langsmith [yes]: yes
use_microsoft_bot_framework [no]: no
openai_model [gpt-4o-mini]: gpt-4o-mini
```

### Passo 3: Configure o ambiente

```bash
# Entre no diretório do projeto gerado
cd news-summarization-agent

# Copie e configure o arquivo de ambiente
cp ENV_VARS.md .env

# Edite o arquivo .env com suas chaves reais
# No mínimo, configure:
# OPENAI_API_KEY=sua_chave_openai_aqui
```

### Passo 4: Instale as dependências

```bash
# Instale as dependências usando uv
uv sync

# Ou, se preferir usar pip
pip install -e .
```

### Passo 5: Execute o projeto

```bash
# Execute usando uv
uv run uvicorn main:app --reload

# Ou usando Python diretamente
python main.py
```

## 2. Testando a API

### Health Check

```bash
curl http://localhost:8000/health
```

### Processamento simples

```bash
curl -X POST http://localhost:8000/news/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Breaking: Scientists discover new method for clean energy production using quantum mechanics.",
    "metadata": {"source": "test", "priority": "high"},
    "options": {"enable_reflection": false}
  }'
```

### Processamento com reflexão

```bash
curl -X POST http://localhost:8000/news/process-with-reflection \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Economic markets show volatility amid global uncertainties. Experts recommend cautious investment strategies.",
    "metadata": {"source": "financial_news"},
    "options": {"enable_reflection": true}
  }'
```

### Schema do workflow

```bash
curl http://localhost:8000/news/schema
```

### Documentação da API

Acesse: http://localhost:8000/docs

## 3. Estrutura Gerada

Após executar o Cookiecutter, você terá a seguinte estrutura:

```
news-summarization-agent/
├── app/
│   ├── presentation/
│   │   └── news_router.py              # Endpoints FastAPI
│   ├── application/
│   │   ├── agent/
│   │   │   └── NewsSummarizationAgent/
│   │   │       ├── agent_builder/      # Construtor do grafo LangGraph
│   │   │       └── node_functions/     # Nós do workflow
│   │   ├── interfaces/                 # Contratos/Protocolos
│   │   └── services/                   # Serviços de aplicação
│   ├── domain/
│   │   ├── entities/                   # Entidades do domínio
│   │   └── state/                      # Estados do LangGraph
│   └── infrastructure/
│       ├── config/                     # Configurações
│       └── llm/                        # Serviços LLM
├── main.py                            # Ponto de entrada FastAPI
├── pyproject.toml                     # Configuração do projeto
├── Dockerfile                         # Container Docker
├── docker-compose.yml                # Orchestração
└── README.md                         # Documentação
```

## 4. Customização do Template

### Adicionando novos nós ao workflow

1. Crie um novo diretório em `app/application/agent/{AgentName}/node_functions/`
2. Implemente a função do nó seguindo o padrão dos existentes
3. Adicione o nó no `agent_builder.py`
4. Atualize o `decision_router.py` se necessário

### Modificando prompts

Os prompts estão localizados nos arquivos `node.py` de cada nó. Customize conforme sua necessidade específica.

### Adicionando novos endpoints

1. Modifique `app/presentation/{domain_name}_router.py`
2. Adicione novos métodos no service se necessário

## 5. Deploy

### Docker

```bash
# Build
docker build -t news-summarization-agent .

# Run
docker run -p 8000:8000 --env-file .env news-summarization-agent
```

### Docker Compose

```bash
docker-compose up --build
```

### Produção

1. Configure as variáveis de ambiente adequadas
2. Use um servidor ASGI robusto (Gunicorn + Uvicorn)
3. Configure monitoramento e logging
4. Implemente health checks adequados

## 6. Integração com Kestra

### Exemplo de task HTTP no Kestra:

```yaml
id: news-summarization-flow
namespace: ai.agents

tasks:
  - id: summarize-news
    type: io.kestra.plugin.core.http.Request
    uri: http://your-agent-url:8000/news/process
    method: POST
    headers:
      Content-Type: "application/json"
    body: |
      {
        "content": "{{ inputs.news_content }}",
        "metadata": {
          "source": "kestra",
          "flow_id": "{{ flow.id }}"
        },
        "options": {
          "enable_reflection": true
        }
      }
```

## 7. Desenvolvimento e Debug

### Logs estruturados

Os logs são configurados usando `structlog` e aparecem em formato JSON no terminal.

### Debug do LangGraph

Use LangSmith (se configurado) para visualizar o fluxo do grafo:

1. Configure `LANGCHAIN_TRACING_V2=true`
2. Configure `LANGCHAIN_API_KEY`
3. Acesse o dashboard do LangSmith

### Testes

```bash
# Execute os testes (quando implementados)
uv run pytest

# Com coverage
uv run pytest --cov=app
```

## 8. Troubleshooting

### Problemas comuns:

1. **Erro de importação**: Verifique se todas as dependências foram instaladas
2. **Erro de configuração**: Confirme se o arquivo `.env` está configurado corretamente
3. **Erro de API OpenAI**: Verifique se sua chave da API está válida e tem créditos
4. **Problemas de performance**: Ajuste o modelo OpenAI ou configurações de timeout

### Verificação rápida:

```bash
# Teste a configuração
uv run python -c "from app.infrastructure.config.config import get_settings; print(get_settings())"

# Teste a conexão com OpenAI
uv run python -c "from app.infrastructure.llm.llm_factory import LLMFactory; llm = LLMFactory.create_default_llm(); print('OpenAI OK')"
```

## 9. Próximos Passos

1. Customize os prompts para seu domínio específico
2. Adicione validações específicas do domínio
3. Implemente testes unitários e de integração
4. Configure CI/CD
5. Adicione métricas e monitoramento
6. Documente seu agente específico

## Suporte

- Consulte o `README.md` do projeto gerado
- Verifique os logs estruturados
- Use o endpoint `/health` para diagnósticos
- Consulte a documentação automática em `/docs`
