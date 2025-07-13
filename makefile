# Makefile para projeto Flask com suporte a Unix, CMD e PowerShell

# Caminhos padrão
PIP=./venv/bin/pip
PYTHON=./venv/bin/python
ACTIVATE=source venv/bin/activate

# Detecta sistema operacional para ajustar comandos
ifeq ($(OS),Windows_NT)
	PIP=venv\\Scripts\\pip.exe
	PYTHON=venv\\Scripts\\python.exe
	ACTIVATE=venv\\Scripts\\activate
endif

# Cria ambiente virtual e instala dependências
setup:
ifeq ($(OS),Windows_NT)
	@if not exist venv (python -m venv venv)
	@call .\\venv\\Scripts\\activate && $(PIP) install -r requirements.txt
	@if exist dev-requirements.txt (call .\\venv\\Scripts\\activate && $(PIP) install -r dev-requirements.txt)
else
	@if [ ! -d "venv" ]; then python -m venv venv; fi
	. venv/bin/activate && $(PIP) install -r requirements.txt
	@if [ -f dev-requirements.txt ]; then . venv/bin/activate && $(PIP) install -r dev-requirements.txt; fi
endif

# Executa a aplicação Flask com FLASK_ENV=development
run:
	@echo "Iniciando aplicação com FLASK_ENV=development"
ifeq ($(OS),Windows_NT)
	@set FLASK_ENV=development&& $(PYTHON) run.py
else
	@FLASK_ENV=development $(PYTHON) run.py
endif

# Cria uma nova migração
migrate:
ifeq ($(OS),Windows_NT)
	@set FLASK_ENV=development&& flask db migrate -m "Nova migração"
else
	@FLASK_ENV=development flask db migrate -m "Nova migração"
endif

# Aplica as migrações
upgrade:
ifeq ($(OS),Windows_NT)
	@set FLASK_ENV=development&& flask db upgrade
else
	@FLASK_ENV=development flask db upgrade
endif

# Verifica estilo de código com flake8
lint:
	$(PYTHON) -m flake8 app

# Executa testes com pytest
test:
	$(PYTHON) -m pytest

# Remove arquivos .pyc e __pycache__
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

# realzia backup do .gitignore 
.PHONY: backup

backup:
    python backup_gitignore.py
