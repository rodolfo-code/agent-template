#!/bin/bash

# Script de Demonstração Rápida do Template Cookiecutter
# Este script demonstra como usar o template para criar um agente

set -e

echo "🚀 DEMONSTRAÇÃO DO TEMPLATE COOKIECUTTER DE MICRO-AGENTES"
echo "========================================================="

# Verificar pré-requisitos
echo "📋 Verificando pré-requisitos..."

if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Instale Python 3.12+"
    exit 1
fi

if ! command -v cookiecutter &> /dev/null; then
    echo "⚠️  Cookiecutter não encontrado. Instalando..."
    pip install cookiecutter
fi

echo "✅ Pré-requisitos verificados"

# Criar configuração de demonstração
echo ""
echo "🔧 Criando configuração de demonstração..."

cat > demo_config.json << EOF
{
    "project_name": "Demo News Agent",
    "project_slug": "demo-news-agent",
    "agent_name": "DemoNewsAgent",
    "domain_name": "demonews",
    "description": "A demo AI agent for news processing",
    "author_name": "Demo User",
    "python_version": "3.12",
    "use_langsmith": "no",
    "use_microsoft_bot_framework": "no",
    "openai_model": "gpt-4o-mini"
}
EOF

echo "✅ Configuração criada: demo_config.json"

# Gerar projeto
echo ""
echo "🏗️  Gerando projeto com Cookiecutter..."

if [ -d "demo-news-agent" ]; then
    echo "⚠️  Removendo projeto existente..."
    rm -rf demo-news-agent
fi

cookiecutter . --no-input --config-file demo_config.json

echo "✅ Projeto gerado: demo-news-agent/"

# Entrar no diretório do projeto
cd demo-news-agent

echo ""
echo "📦 Configurando ambiente do projeto..."

# Criar arquivo .env de demonstração
cat > .env << EOF
# Demo environment - NÃO USE EM PRODUÇÃO
OPENAI_API_KEY=demo_key_aqui_substitua_por_uma_chave_real
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

# Application Configuration
ENVIRONMENT=demo
LOG_LEVEL=INFO
DEBUG=true

# FastAPI Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# DemoNewsAgent Configuration
DEMONEWSAGENT_MAX_RETRIES=3
DEMONEWSAGENT_TIMEOUT=30
DEMONEWSAGENT_ENABLE_REFLECTION=true

# Additional Configuration
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=60
ENABLE_CORS=true
EOF

echo "✅ Arquivo .env criado"

# Verificar se uv está disponível
if command -v uv &> /dev/null; then
    echo "📦 Instalando dependências com uv..."
    uv sync --no-dev
    echo "✅ Dependências instaladas com uv"
else
    echo "⚠️  uv não encontrado. Para instalar dependências, execute:"
    echo "   pip install uv && uv sync"
fi

echo ""
echo "📁 Estrutura do projeto gerada:"
echo "============================================"
find . -type f -name "*.py" -o -name "*.toml" -o -name "*.yml" -o -name "*.md" | head -15
echo "... (e mais arquivos)"

echo ""
echo "🔧 Verificação da estrutura..."

# Verificar arquivos essenciais
essential_files=(
    "main.py"
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    "README.md"
    ".env"
    "app/presentation/demonews_router.py"
    "app/infrastructure/config/config.py"
)

missing_files=()
for file in "${essential_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -eq 0 ]]; then
    echo "✅ Todos os arquivos essenciais foram criados"
else
    echo "❌ Arquivos faltando: ${missing_files[*]}"
fi

echo ""
echo "🧪 INSTRUÇÕES PARA TESTAR:"
echo "=========================="
echo ""
echo "1. Configure sua chave OpenAI no arquivo .env:"
echo "   OPENAI_API_KEY=sua_chave_real_aqui"
echo ""
echo "2. Execute o agente:"
if command -v uv &> /dev/null; then
    echo "   uv run uvicorn main:app --reload"
else
    echo "   pip install -e ."
    echo "   python main.py"
fi
echo ""
echo "3. Teste a API:"
echo "   curl http://localhost:8000/health"
echo "   open http://localhost:8000/docs"
echo ""
echo "4. Teste processamento:"
echo "   curl -X POST http://localhost:8000/demonews/process \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"content\": \"Breaking news: AI revolutionizes development!\"}'"
echo ""
echo "📊 ESTATÍSTICAS DO PROJETO:"
echo "==========================="
echo "Total de arquivos Python: $(find . -name "*.py" | wc -l)"
echo "Total de arquivos config: $(find . -name "*.toml" -o -name "*.yml" -o -name "*.yaml" | wc -l)"
echo "Linhas de código (aprox): $(find . -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "N/A")"

echo ""
echo "📚 DOCUMENTAÇÃO:"
echo "================"
echo "- README.md              : Documentação principal"
echo "- ENV_VARS.md           : Variáveis de ambiente"
echo "- COMO_USAR_TEMPLATE.md : Guia completo de uso"
echo "- EXEMPLO_USO.md        : Exemplo prático completo"

echo ""
echo "🎉 DEMONSTRAÇÃO CONCLUÍDA!"
echo "=========================="
echo ""
echo "O template gerou com sucesso um micro-agente Python completo com:"
echo "✅ Clean Architecture"
echo "✅ FastAPI com documentação automática"
echo "✅ LangGraph workflow com reflexão"
echo "✅ Configuração Docker completa"
echo "✅ Integração Kestra pronta"
echo "✅ Logging estruturado"
echo "✅ Testes e validações"
echo ""
echo "📍 Localização: $(pwd)"
echo ""
echo "Para próximos passos, consulte o README.md ou execute:"
echo "cd demo-news-agent && cat README.md"

# Limpeza
cd ..
rm -f demo_config.json

echo ""
echo "🚀 Template pronto para uso! Happy coding! 🎯" 