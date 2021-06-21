from collections import UserString
from app.utils import format_data_housing, house_results_to_dataframe
import click
import pandas as pd
from flask.cli import with_appcontext
from app.database.db import db
from app.database.models import House, User, UserRole, ModelParams
from getpass import getpass
from werkzeug.security import generate_password_hash
from consolemenu import SelectionMenu

from app.utils import regression


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""
    data_housing = pd.read_csv("housing.csv")
    data_housing = format_data_housing(data_housing)
    House.insert_from_pd(data_housing)
    print("Données dans la BDD insérées")
    roles = [
        UserRole(
            name="Admin",
            permissions=[
                "admin.read",
                "admin.write",
                "admin.update",
                "user.read",
                "user.write",
                "user.update",
            ],
        ),
        UserRole(name="Membre", permissions=["user.read"]),
    ]
    for role in roles:
        db.session.add(role)
    print("Roles ajoutées")
    db.session.add(ModelParams(alpha=0.0001, l1_ratio=0, max_iter=700, active=True))
    print("Paramètres du modèle par défaut ajoutés")
    db.session.commit()
    print("Tout a été inséré dans la base de données !")


@click.command("create-user")
@with_appcontext
def create_user():
    """Insert un utilisateur la base de données de l'application"""
    roles = UserRole.query.all()
    role = SelectionMenu.get_selection([role.name for role in roles], title="Sélectionner un rôle d'utilisateur", show_exit_option=False)
    role_id = roles[role].id
    print(f"Ajout d'un utilisateur appartenant au groupe {roles[role].name}")
    email = input("Entrez votre addresse mail : ")
    password = getpass("Entrer le mot de passe utilisateur : ")
    confirm_password = getpass("Veuillez confirmer votre mot de passe : ")
    if confirm_password == password:
        insert_user = User(email=email, password=generate_password_hash(password), role_id=role_id)
        db.session.add(insert_user)
        db.session.commit()
        print("Utilisateur ajouté !")
    else:
        print("Mot de passe non identique")

@click.command("predict-value")
@with_appcontext
def predict_value():
    """Prédit la valeur médiane d'une maison
    """
    mp = ModelParams.query.filter_by(active=True).first()
    if mp is None:
        return
    data = pd.read_sql("SELECT * FROM house", db.engine)
    data = house_results_to_dataframe(data)
    ocean_proximity = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]
    d_test = {
                "longitude": [float(input("Longitude ? "))],
                "latitude": [float(input("Latitude ? "))],
                "housing_median_age": [int(input("Age médian d'une maison ? "))],
                "total_rooms": [int(input("Superficie totale des pièces ? "))],
                "total_bedrooms": [int(input("Superficie totale des chambres ? "))],
                "population": [int(input("Population dans le block ? "))],
                "households": [int(input("Nombre d'habitant d'une maison ? "))],
                "median_income": [float(input("Revenu médian des habitants d'un block ? "))],
                "ocean_proximity": [ocean_proximity[SelectionMenu.get_selection(ocean_proximity, "Proximité vers l'océan ? ", show_exit_option=False)]],
            }
    revenu_median = input("Prix médian réel ? (defaut : None)")
    if revenu_median != "":
        revenu_median = float(revenu_median)
    else:
        revenu_median = None
    y = regression(data, pd.DataFrame.from_dict(d_test), revenu_median, mp)
    print(f"Prix médian prédit : {y}")