from flask import Flask
from flask_migrate import Migrate
import json
import os

from app import controllers
from app.db import db
from app.db_commands import insert_db, create_user, predict_value
from app.services import login_manager

def create_app(test_config=None):
    # On initialise l'app flask 
    app = Flask(__name__, instance_relative_config=True)
    
    # On initialise flask-migrate pour les outils de migration de la BDD
    migrate = Migrate()

    # Configuration de l'application
    # On récupère en premier la configuration d'un fichier config.json présent dans /instance/config.json
    # Tout d'abord on vérifie que le fichier config.json est bien présent dans le dossier instance
    if os.path.isfile(app.instance_path + '/config.json'):
        # S'il est présent, on charge la configuration de celui-ci dans l'app flask
        app.config.from_file("config.json", load=json.load)
        # Dans le cas où DEFAULT_DB est bien présent dans la config, on met en place la configuration de SQLAlchemy en fonction des éléments présents dans config.json
        if "DEFAULT_DB" in app.config:
            # On récupère la config de la base de données à utiliser par défaut du config.json
            dbconfig = app.config[app.config["DEFAULT_DB"]]
            app.config.from_mapping(
                {
                    "SQLALCHEMY_DATABASE_URI": f"{dbconfig['connector']}://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['bdd']}",
                    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                }
            )
    else:
        # Au cas où il n'existe pas, on avertit que celui-ci n'est pas présent
        app.logger.warn("Aucun fichier config.json n'est présent dans le dossier /instance/. L'application risque de mal fonctionner !")

    # Si la variable d'environnement (défini via terminal ou dans le fichier .env à la racine du dossier) SQLALCHEMY_DATABASE_URI existe
    # On remplace la config de connexion à la base de données par cette variable environnment
    if "SQLALCHEMY_DATABASE_URI" in os.environ:
        app.config.from_mapping({
            "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"]
        })
    
    # Dans le cas de tests, on passe directement la configuration à create_app, la config de test doit donc remplacer toutes les configs précédentes
    if test_config is not None:
        app.config.from_mapping(test_config)


    # On initialise SQLAlchemy avec les éléments de config à la BDD
    db.init_app(app)

    # On importe les models afin que flask_migrate les connaisse
    from app.models import User, House, UserRole, ModelParams

    # On initialise l'outil de migration
    migrate.init_app(app, db)

    # On ajoute la commande "flask insert-db" à l'application
    app.cli.add_command(insert_db)

    # On ajoute la commande "flask create-user" à l'application
    app.cli.add_command(create_user)

    # On ajoute la commande "flask predict-value" à l'application
    app.cli.add_command(predict_value)

    # instancie le service de login qui va manager l'aspect login/logout/cookie/session
    login_manager.init_app(app)

    # On enregistre les différents controllers pour les routes
    controllers.init_app(app)

    # L'application est prete, on la retourne
    return app