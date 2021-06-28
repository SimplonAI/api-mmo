from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, RadioField, StringField, SelectMultipleField
from wtforms.fields.html5 import EmailField, IntegerField, DecimalRangeField, IntegerRangeField
from wtforms.validators import DataRequired


ocean_proximity = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]


# Chaque formulaire hérite de Flask-WTF afin de gérer plus facilement la validation des données et la génération des champs HTML

class LoginForm(FlaskForm):
    """Formulaire de connexion
    """
    email = EmailField('Adresse e-mail', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')


class PredictForm(FlaskForm): 
    """ Formulaire de prédiction
    """
    adresse = StringField("Adresse", validators=[DataRequired()])
    adresse2 = StringField("Adresse 2", validators=[DataRequired()])
    ville = StringField("Ville", validators=[DataRequired()])
    etat = StringField("État", validators=[DataRequired()])
    code_postal = IntegerField("Code Postal", validators=[DataRequired()])
    median_age = IntegerField("Âge moyen du foyer", validators=[])
    total_rooms = IntegerField("Nombres de pièces", validators=[])
    total_bedrooms = IntegerField("Nombre de chambres", validators=[])
    population = IntegerField("Population", validators=[])
    households = IntegerField("Nombres de personnes composant le foyer", validators=[])
    median_income = IntegerField("Revenu médian", validators=[])
    ocean_proximity = RadioField("Proximité à l'océan", choices =ocean_proximity, validators=[])


class DashboardForm(FlaskForm):
    """Formulaire de personalisation du dashboard
    """
    plots = SelectMultipleField('Graphiques')


class ModelParamsForm(FlaskForm):
    alpha = DecimalRangeField("Alpha", places=5)
    l1_ratio = DecimalRangeField("L1 Ratio", places=5)
    max_iter = IntegerField("Max Iter")
    active = BooleanField("Actif")