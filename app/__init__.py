from flask import Flask
from flask_migrate import Migrate
import json
import os

from app.database.db import db
from app.controllers import main_controller
from app.db_commands import insert_db, create_user

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if os.path.isfile(app.instance_path + '/config.json'):
        app.config.from_file("config.json", load=json.load)

    if "DEFAULT_DB" in app.config:
        dbconfig = app.config[app.config["DEFAULT_DB"]]
        app.config.from_mapping(
            {
                "SQLALCHEMY_DATABASE_URI": f"{dbconfig['connector']}://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['bdd']}",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )

    if "SQLALCHEMY_DATABASE_URI" in os.environ:
        app.config.from_mapping({
            "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"]
        })
    
    if test_config is not None:
        app.config.from_mapping(test_config)


    # On initialise SQLAlchemy avec les éléments de config à la BDD
    db.init_app(app)

    # On importe les models afin que flask_migrate les connaisse
    from app.database.models import User, House, UserRole, ModelParams

    # On initialise l'outil de migration
    migrate.init_app(app, db)

    # On ajoute la commande "flask insert-db" à l'application
    app.cli.add_command(insert_db)

    # On ajoute la commande "flask create-user" à l'application
    app.cli.add_command(create_user)

    # On enregistre les différents controllers pour les routes
    # On ajoute le controller pour les urls de haut niveau ("/", "/login", "/contact", ...)
    app.register_blueprint(main_controller)
    return app