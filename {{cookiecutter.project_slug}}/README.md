# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Visão Geral

O **{{ cookiecutter.agent_name }}** é um micro-agente especializado desenvolvido com Clean Architecture, integrado com FastAPI, LangGraph, LangChain e OpenAI. Este projeto segue as melhores práticas de desenvolvimento e é otimizado para integração com Kestra.

## Arquitetura

Este projeto implementa Clean Architecture com as seguintes camadas:

- **Presentation**: Endpoints FastAPI e roteadores
- **Application**: Lógica de negócio, serviços e agentes
- **Domain**: Entidades e estados do domínio
- **Infrastructure**: Configurações e serviços externos (LLM, banco de dados)

## Tecnologias Utilizadas

- **Python {{ cookiecutter.python_version }}**
- **FastAPI** - Framework web moderno e rápido
- **LangGraph** - Framework para construção de agentes com grafos
- **LangChain** - Framework para aplicações com LLM
- **OpenAI** - Modelos de linguagem ({{ cookiecutter.openai_model }})
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **uv** - Gerenciador de pacotes Python ultrarrápido
  {% if cookiecutter.use_langsmith == "yes" -%}
- **LangSmith** - Monitoramento e debugging de LLM
  {% endif -%}

## Pré-requisitos

- Python {{ cookiecutter.python_version }}+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes)
- Docker e Docker Compose (opcional)

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd {{ cookiecutter.project_slug }}
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Instale as dependências

```bash
uv sync
```

### 4. Execute o projeto

```bash
uv run uvicorn main:app --reload
```

## Configuração

### Variáveis de Ambiente Obrigatórias

- `OPENAI_API_KEY`: Sua chave da API OpenAI
  {% if cookiecutter.use_langsmith == "yes" -%}
- `LANGCHAIN_API_KEY`: Sua chave da API LangSmith (opcional)
  {% endif -%}

### Variáveis de Ambiente Opcionais

- `OPENAI_MODEL`: Modelo OpenAI a ser usado (padrão: {{ cookiecutter.openai_model }})
- `LOG_LEVEL`: Nível de log (padrão: INFO)
- `ENVIRONMENT`: Ambiente de execução (padrão: development)

## Uso com Docker

### Desenvolvimento

```bash
docker-compose up --build
```

### Produção

```bash
docker build -t {{ cookiecutter.project_slug }} .
docker run -p 8000:8000 --env-file .env {{ cookiecutter.project_slug }}
```

## Estrutura do Projeto

```
{{ cookiecutter.project_slug }}/
├── app/
│   ├── presentation/           # Camada de apresentação (FastAPI)
│   │   └──
│   ├── application/           # Camada de aplicação
│   │   ├── agent/
│   │   │   └── {{ cookiecutter.agent_name }}/
│   │   │       ├── agent_builder/
│   │   │       └── node_functions/
│   │   ├── interfaces/
│   │   └── services/
│   ├── domain/               # Camada de domínio
│   │   ├── entities/
│   │   └── state/
│   └── infrastructure/       # Camada de infraestrutura
│       ├── config/
│       └── llm/
├── main.py                  # Ponto de entrada da aplicação
├── pyproject.toml          # Configuração do projeto e dependências
├── Dockerfile             # Configuração Docker
└── docker-compose.yml     # Configuração Docker Compose
```

## API Endpoints

- `GET /health` - Health check da aplicação

Para documentação completa da API, acesse: http://localhost:8000/docs

## Desenvolvimento

### Testes

```bash
uv run pytest
```

### Formatação de código

```bash
uv run black .
uv run isort .
```

### Linting

```bash
uv run flake8
uv run mypy .
```

## Integração com Kestra

Este agente foi desenvolvido para integração com Kestra. Para usar com Kestra:

1. Configure o endpoint HTTP task apontando para `http://localhost:8000
2. Configure as variáveis de ambiente necessárias no Kestra
3. Use o payload apropriado conforme a documentação da API

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

**{{ cookiecutter.author_name }}**

## Changelog

### v0.1.0 (Initial Release)

- Implementação inicial do {{ cookiecutter.agent_name }}
- Integração com FastAPI, LangGraph e OpenAI
- Estrutura Clean Architecture
- Configuração Docker e Docker Compose
