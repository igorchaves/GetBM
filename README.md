# 📊 Gestão Backlog (GetBM)

O GetBM é um sistema desenvolvido para automatizar a criação e atualização de organogramas de backlog de projetos. Ele visa eliminar processos manuais suscetíveis a erros, oferecendo uma visualização moderna, interativa e de fácil manutenção baseada em cadastros estruturados.

# 🚀 Tecnologias Utilizadas

Python (Flask)
Pyvis – Visualização de organogramas interativos
PostgreSQL / SQLite / MongoDB – Armazenamento de dados
HTML/CSS/JS – Interface web

# 🔧 Cadastro de:

- Funcionalidades
- Status
- Categorias 
- Sprint

Gerenciamento (Configurações): 
- Projetos
- Usuário

Funcionalidades Centrais da aplicação: 
- Backlog
- Organograma

Geração automática de organogramas com:
- Subníveis ilimitados
- Zoom, arraste e tooltips
- Filtros por status (implementado, homologado etc.)
- Exportação para PDF ou imagem

# 🛠️ Etapas de Desenvolvimento

- ✅ Levantamento de requisitos
- 🔜 Implementação do backend
- 🚧 Criação da interface web <- Fase atual
- 🔜 Integração com Pyvis (Organograma)
- 🔜 Testes e validação
- 🔜 Implantação

# 📦 Instalação e Execução

Pré-requisitos:
- Python 3.10+
- pip
- (opcional) Ambiente virtual

Passos
# Clone o repositório
- git clone https://github.com/seu-usuario/getbm.git
- cd getbm

# Crie e ative um ambiente virtual (opcional)

- python -m venv venv
- source venv/bin/activate  # Linux/macOS
- venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python run.py


# ✅ Recomendação Técnica

O uso do Pyvis é recomendado por seu equilíbrio entre simplicidade, interatividade e visual moderno, ideal para representar estruturas hierárquicas como backlogs.
