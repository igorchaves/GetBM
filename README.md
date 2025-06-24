# 📊 Gestão Backlog (GetBM)

GetBM é uma aplicação web para automatizar a criação e visualização de organogramas de backlog de projetos. Com uma interface moderna e interativa, permite o cadastro estruturado de projetos, funcionalidades e especificações, gerando visualizações dinâmicas e exportáveis.

# 🚀 Tecnologias Utilizadas

Python (Flask)
Pyvis – Visualização de organogramas interativos
PostgreSQL / SQLite / MongoDB – Armazenamento de dados
HTML/CSS/JS – Interface web

# 🔧 Funcionalidades Cadastro de:

Projetos
Funcionalidades
Especificações
Geração automática de organogramas com:
Subníveis ilimitados
Zoom, arraste e tooltips
Filtros por status (implementado, homologado etc.)
Exportação para PDF ou imagem

# 🛠️ Etapas de Desenvolvimento

Levantamento de requisitos <- Concluida 
Implementação do backend
Criação da interface web <- Fase atual
Integração com Pyvis
Testes e validação
Implantação

# 📦 Instalação e Execução

Pré-requisitos
Python 3.10+
pip
(opcional) Ambiente virtual

Passos
# Clone o repositório
git clone https://github.com/seu-usuario/getbm.git
cd getbm

# Crie e ative um ambiente virtual (opcional)

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python run.py


# ✅ Recomendação Técnica

O uso do Pyvis é recomendado por seu equilíbrio entre simplicidade, interatividade e visual moderno, ideal para representar estruturas hierárquicas como backlogs.
