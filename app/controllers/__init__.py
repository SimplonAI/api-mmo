from flask import Flask
from .main import main_blueprint
from .api import api_blueprint


def init_app(app: Flask):
    # On ajoute les controller pour les urls de haut niveau ("/", "/login", "/contact", ...)
    app.register_blueprint(main_blueprint)
    # On ajoute les controller pour les urls api ("/api/regression", "/api/plot",  ...)
    app.register_blueprint(api_blueprint)