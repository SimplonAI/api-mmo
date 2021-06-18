import click
import pandas as pd
from flask.cli import with_appcontext
from app.database.db import db
from app.database.models import Utilisateur
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash



@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application
    """
    data_housing = pd.read_csv("housing.csv")
    data_housing["total_bedrooms"] = data_housing["total_bedrooms"].fillna(
        data_housing["total_bedrooms"].median()
    )
    data_housing[
        [
            "population",
            "housing_median_age",
            "total_rooms",
            "total_bedrooms",
            "households",
            "median_house_value",
        ]
    ] = data_housing[
        [
            "population",
            "housing_median_age",
            "total_rooms",
            "total_bedrooms",
            "households",
            "median_house_value",
        ]
    ].astype(
        int
    )
    data_housing = data_housing.rename(
        columns={
            "longitude": "ho_longitude",
            "latitude": "ho_latitude",
            "housing_median_age": "ho_housing_median_age",
            "total_rooms": "ho_total_rooms",
            "total_bedrooms": "ho_total_bedrooms",
            "population": "ho_population",
            "households": "ho_households",
            "median_income": "ho_median_income",
            "median_house_value": "ho_median_house_value",
            "ocean_proximity": "ho_ocean_proximity",
        }
    )
    data_housing.index += 1
    data_housing.rename_axis(index="ho_id")
    data_housing.to_sql("house", if_exists="append", con=db.engine, index=False)
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
    
    
        