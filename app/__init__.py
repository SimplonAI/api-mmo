import os

from flask import Flask
from flask_migrate import Migrate
import json

from app.database.db import db
from app.controllers import main_controller
from app.insert_db import insert_db, create_user


migrate = Migrate()


def create_app(config_name):


    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        
        #app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')


    

    # On initialise SQLAlchemy avec les éléments de config à la BDD
    db.init_app(app)

    # On importe les models afin que flask_migrate les connaisse
    from app.database.models import Utilisateur, House

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
