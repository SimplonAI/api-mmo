from flask import Flask
import json

from app.database.db import db
from app.controllers import main_controller

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_file("config.json", load=json.load)
    
    db.init_app(app)
    
    app.register_blueprint(main_controller)
    return app