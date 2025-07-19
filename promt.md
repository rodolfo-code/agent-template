# Prompt para Code LLM: Geração de Template Cookiecutter para Micro-Agentes Python

Quero que você atue como um engenheiro de software especializado em automação de scaffolding de projetos Python, com foco em Clean Architecture, agentes de IA e integração com Kestra.

## Contexto

Eu desenvolvo micro-agentes Python especialistas em tarefas únicas, integrados com Kestra. Para cada novo agente, preciso de uma estrutura de projeto robusta, baseada em Clean Architecture, com integração a FastAPI, LangGraph, LangChain, OpenAI, e containerização via Docker. Atualmente, uso o package manager [uv](https://github.com/astral-sh/uv) e mantenho todas as dependências e configurações modernas.

## Objetivo

Me ajude a construir, passo a passo, um template de Cookiecutter que gere automaticamente a estrutura de um novo agente, permitindo customizar dinamicamente:

- Nome do projeto (slug)
- Nome da classe principal do agente
- Nome do domínio (ex: "news", "document", etc.)
- Descrição do agente

## Requisitos do template

- Estrutura de pastas baseada em Clean Architecture, conforme o exemplo abaixo.
- Todos os arquivos, pastas e nomes de classes que contenham "summarization", "news" ou similares devem ser dinâmicos, substituídos por variáveis do Cookiecutter.
- O template deve gerar:
  - `pyproject.toml` e `uv.lock` já configurados para FastAPI, Uvicorn, LangGraph, LangChain, OpenAI, LangSmith, Pydantic, python-dotenv, Microsoft Bot Framework, aiohttp, e logging.
  - Dockerfile e docker-compose.yml prontos para Python 3.12-slim e uv.
  - `.env` de exemplo com variáveis como `OPENAI_API_KEY`.
  - `.gitignore`, `.python-version` e um `README.md` com as informações customizadas.
  - `main.py` como ponto de entrada FastAPI, já importando o router do agente.
  - Estrutura de pastas conforme abaixo, com todos os nomes dinâmicos:
    ```
    {{ cookiecutter.project_slug }}/
    ├── pyproject.toml
    ├── uv.lock
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env
    ├── .gitignore
    ├── .python-version
    ├── main.py
    └── app/
        ├── presentation/
        │   └── {{ cookiecutter.domain_name }}_router.py
        ├── application/
        │   ├── agent/
        │   │   └── {{ cookiecutter.agent_name }}/
        │   │       ├── agent_builder/
        │   │       │   ├── decision_router.py
        │   │       │   └── {{ cookiecutter.agent_name }}_agent_builder.py
        │   │       └── node_functions/
        │   │           ├── adjust_{{ cookiecutter.agent_name }}_node/
        │   │           ├── reflect_node/
        │   │           └── {{ cookiecutter.agent_name }}_node/
        │   ├── interfaces/
        │   │   └── illm_service.py
        │   └── services/
        │       └── {{ cookiecutter.agent_name }}_service.py
        ├── domain/
        │   ├── entities/
        │   │   ├── {{ cookiecutter.domain_name }}.py
        │   │   └── {{ cookiecutter.agent_name }}_output.py
        │   └── state/
        │       └── {{ cookiecutter.agent_name }}_state.py
        └── infrastructure/
            ├── config/
            │   └── config.py
            └── llm/
                ├── llm_factory.py
                └── openai_service.py
    ```
- O template deve ser fácil de evoluir e versionar.
- Explique cada etapa antes de mostrar o código.
- Mostre o conteúdo de cada arquivo gerado, usando as variáveis do Cookiecutter.
- Oriente como testar o template localmente.
- Sugira boas práticas para evoluir o template no futuro.

## Fluxo desejado

1. Comece pela definição da estrutura de pastas e do arquivo `cookiecutter.json` com todas as variáveis necessárias.
2. Siga para os arquivos de configuração e dependências.
3. Depois, mostre exemplos dos arquivos Python principais, sempre usando as variáveis dinâmicas.
4. Aguarde minha confirmação a cada etapa antes de prosseguir.
