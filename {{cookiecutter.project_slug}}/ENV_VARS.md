# Variáveis de Ambiente

Este arquivo documenta todas as variáveis de ambiente necessárias para o {{ cookiecutter.project_name }}.

## Configuração Obrigatória

### OpenAI

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL={{ cookiecutter.openai_model }}
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000
```

{% if cookiecutter.use_langsmith == "yes" -%}

### LangSmith (Opcional - para monitoramento)

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT={{ cookiecutter.project_slug }}
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

{% endif -%}

{% if cookiecutter.use_microsoft_bot_framework == "yes" -%}

### Microsoft Bot Framework (Opcional)

```bash
MICROSOFT_APP_ID=your_microsoft_app_id_here
MICROSOFT_APP_PASSWORD=your_microsoft_app_password_here
```

{% endif -%}

## Configuração da Aplicação

```bash
# Ambiente
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# FastAPI
HOST=0.0.0.0
PORT=8000
RELOAD=true

# {{ cookiecutter.agent_name }} Específico
{{ cookiecutter.agent_name.upper() }}_MAX_RETRIES=3
{{ cookiecutter.agent_name.upper() }}_TIMEOUT=30
{{ cookiecutter.agent_name.upper() }}_ENABLE_REFLECTION=true

# Configurações Adicionais
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=60
ENABLE_CORS=true
```

## Configurações Opcionais

### Banco de Dados (se necessário)

```bash
DATABASE_URL=sqlite:///./{{ cookiecutter.project_slug }}.db
```

### Redis (se necessário)

```bash
REDIS_URL=redis://localhost:6379/0
```

## Como usar

1. Copie as variáveis necessárias para um arquivo `.env` na raiz do projeto
2. Substitua os valores pelos seus dados reais
3. O arquivo `.env` será automaticamente carregado pela aplicação

## Exemplo de arquivo .env

```bash
# Salve este conteúdo em um arquivo chamado .env

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-key-here
OPENAI_MODEL={{ cookiecutter.openai_model }}
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

{% if cookiecutter.use_langsmith == "yes" -%}
# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your-actual-langsmith-key-here
LANGCHAIN_PROJECT={{ cookiecutter.project_slug }}
{% endif -%}

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# FastAPI Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# {{ cookiecutter.agent_name }} Configuration
{{ cookiecutter.agent_name.upper() }}_MAX_RETRIES=3
{{ cookiecutter.agent_name.upper() }}_TIMEOUT=30
{{ cookiecutter.agent_name.upper() }}_ENABLE_REFLECTION=true
```
