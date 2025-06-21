from flask import Flask
from app.routes import app as app_routes

app = Flask(__name__)

# Registro das rotas
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run(debug=True)

