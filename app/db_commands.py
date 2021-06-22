from collections import UserString
import click
import pandas as pd
from flask.cli import with_appcontext
from getpass import getpass
from werkzeug.security import generate_password_hash
from consolemenu import SelectionMenu

from app.db import db
from app.utils import format_data_housing, house_results_to_dataframe, regression
from app.models import House, User, UserRole, ModelParams


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""
    # On récupère les données du fichier CSV dans un dataframe
    data_housing = pd.read_csv("housing.csv")
    # On format les données (int64 pour les champs) afin de les préparer à l'insertion
    data_housing = format_data_housing(data_housing)
    # On insère les données dans la table House
    House.insert_from_pd(data_housing)
    print("Données dans la BDD insérées")
    
    # On crée les roles Admin et Membre avec des permissions différentes
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
    # On ajoute chaque rôle à la BDD
    for role in roles:
        db.session.add(role)
    print("Roles ajoutées")

    # On ajout les 1ers paramètres du modèle pour la régression 
    db.session.add(ModelParams(alpha=0.0001, l1_ratio=0, max_iter=700, active=True))
    print("Paramètres du modèle par défaut ajoutés")
    
    # On confirme tous les changements pour la transaction
    db.session.commit()
    print("Tout a été inséré dans la base de données !")


@click.command("create-user")
@with_appcontext
def create_user():
    """Insert un utilisateur la base de données de l'application"""
    # On récupère tous les roles utilisateurs possibles présents de la BDD
    roles = UserRole.query.all()

    # On affiche un menu de sélection du rôle pour le nouvel utilisateur et on récupère la sélection
    index = SelectionMenu.get_selection([role.name for role in roles], title="Sélectionner un rôle d'utilisateur", show_exit_option=False)

    print(f"Ajout d'un utilisateur appartenant au groupe {roles[index].name}")
    # On demande l'adresse e-mail
    email = input("Entrez votre addresse mail : ")
    # On demande le mot de passe
    password = getpass("Entrer le mot de passe utilisateur : ")
    confirm_password = getpass("Veuillez confirmer votre mot de passe : ")
    
    # On vérifie que les mots de passes tapées soient les mêmes
    if confirm_password == password:
        # On crée un nouvel utilisateur avec les champs renseignés et le role_id
        insert_user = User(email=email, password=generate_password_hash(password), role_id=roles[index].id)
        # On l'ajoute à la BDD
        db.session.add(insert_user)
        # On confirme les changements de la transaction
        db.session.commit()
        print("Utilisateur ajouté !")
    else:
        print("Mot de passe non identique")

@click.command("predict-value")
@with_appcontext
def predict_value():
    """Prédit la valeur médiane d'une maison
    """
    # On récupère les paramètres de modélisation actifs
    mp = ModelParams.query.filter_by(active=True).first()
    # Si aucun paramètres dans la BDD, on quitte la fonction
    if mp is None:
        return
    
    # On récupère toutes les maisons de la BDD via pandas
    data = pd.read_sql("SELECT * FROM house", db.engine)
    # On renomme les colonnes du dataframe pour correspondre à ceux du csv
    data = house_results_to_dataframe(data)

    # Variable nécessaire pour créer le menu de sélection
    ocean_proximity = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]

    # On demande les données nécessaire à la prédiction puis on les stock dans un dictionnaire
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
    
    # On demande le prix réel de la maison s'il est connu
    revenu_median = input("Prix médian réel ? (defaut : None)")
    if revenu_median != "":
        revenu_median = float(revenu_median)
    else:
        revenu_median = None
    # On prédit le prix
    r_score, y, rmse = regression(data, pd.DataFrame.from_dict(d_test), revenu_median, mp)
    print(f"R² : {r_score}")
    if rmse is not None:
        print(f"MSRE : +/- {rmse}")

    print(f"Prix médian prédit : {y}")