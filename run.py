import os
import sys
import subprocess
from dotenv import load_dotenv
from app import create_app

# Carrega o .env com base no FLASK_ENV
env = os.getenv("FLASK_ENV", "development")
dotenv_file = f".env.{env}"
load_dotenv(dotenv_file)

# Executa auto_migrate.py se for ambiente de desenvolvimento
if env == "development" and os.getenv("AUTO_MIGRATE", "false").lower() == "true":
    try:
        subprocess.run([sys.executable, "auto_migrate.py"], check=True)
    except subprocess.CalledProcessError as e:
      print(f"Erro ao executar auto_migrate.py: {e}")

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
