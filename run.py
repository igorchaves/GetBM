import os
import sys
import subprocess
from dotenv import load_dotenv
from app import create_app

# Carrega o .env.development
load_dotenv(".env.development")

# Executa auto_migrate.py se for ambiente de desenvolvimento
if os.getenv("FLASK_ENV") == "development" and os.getenv("AUTO_MIGRATE", "false").lower() == "true":
    subprocess.run([sys.executable, "auto_migrate.py"])

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
