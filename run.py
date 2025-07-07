import os
import sys
import subprocess
from dotenv import load_dotenv
from app import create_app

env = os.getenv("FLASK_ENV", "development")
dotenv_file = f".env.{env}"
load_dotenv(dotenv_file)

app = create_app()

if __name__ == '__main__':
    if env == "development" and os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        try:
            print("🔄 Executando auto_migrate.py...")
            subprocess.run([sys.executable, "auto_migrate.py"], check=True)
            print("✅ Migração automática concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar auto_migrate.py: {e}")
        except FileNotFoundError:
            print("❌ Arquivo auto_migrate.py não encontrado.")

    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, use_reloader=True)