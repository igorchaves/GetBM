import os
from flask import Flask
from flask_migrate import upgrade, migrate
from app import create_app, db

app = create_app()

with app.app_context():
    migrate(message="Auto migration")
    upgrade()