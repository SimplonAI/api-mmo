from app.utils import format_data_housing
import click
import pandas as pd
from flask.cli import with_appcontext
from app.database.db import db
from app.database.models import House, Utilisateur
from getpass import getpass
from werkzeug.security import generate_password_hash



@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application
    """
    data_housing = pd.read_csv("housing.csv")
    data_housing = format_data_housing(data_housing)
    House.insert_from_pd(data_housing)
    print("Tout a été inséré dans la base de données !")

@click.command("create-user")
@with_appcontext
def create_user():
    """Insert un utilisateur la base de données de l'application
    """

    mail = input("Entrez votre addresse mail : ")
    password = getpass("Entrer le mot de passe utilisateur : ")
    confirm_password = getpass("Veuillez confirmer votre mot de passe : ")
    if confirm_password == password:
        insert_user = Utilisateur(mail=mail, password=generate_password_hash(password))
        db.session.add(insert_user)
        db.session.commit()
        print("Utilisateur ajouté !")
    else:
        print("Mot de passe non identique")
    
    
        