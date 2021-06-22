from flask import Flask
from .main import main_controller
from .api import api_controller


def init_app(app: Flask):
    app.register_blueprint(main_controller)
    app.register_blueprint(api_controller)