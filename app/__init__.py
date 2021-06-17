from flask import Flask
import json

from app.database.db import db
from app.controllers import main_controller
from app.insert_db import insert_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_file("config.json", load=json.load)
    else:
        app.config.from_mapping(test_config)

    if "default_db" in app.config:
        dbconfig = app.config[app.config["default_db"]]
        app.config.from_mapping(
            {
                "SQLALCHEMY_DATABASE_URI": f"{dbconfig['connector']}://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['bdd']}",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False
            }
        )

    # On initialise SQLAlchemy avec les éléments de config à la BDD
    db.init_app(app)

    # On ajoute la commande "flask insert-db" à l'application
    app.cli.add_command(insert_db)

    # On enregistre les différents controllers pour les routes
    # On ajoute le controller pour les urls de haut niveau ("/", "/login", "/contact", ...)
    app.register_blueprint(main_controller)

    return app
