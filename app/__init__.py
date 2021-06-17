from flask import Flask
import json

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_file("config.json", load=json.load)
        @app.route("/")
        def index():
            return "Hello World ! Agile"
    return app