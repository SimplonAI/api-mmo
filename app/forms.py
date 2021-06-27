from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import PasswordField, BooleanField, RadioField, StringField, SelectMultipleField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired


ocean_proximity = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]


=======
from wtforms import PasswordField, BooleanField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
# Chaque formulaire hérite de Flask-WTF afin de gérer plus facilement la validation des données et la génération des champs HTML

class LoginForm(FlaskForm):
    """Formulaire de connexion
    """
    email = EmailField('Adresse e-mail', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')

<<<<<<< HEAD
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
=======
class DashboardForm(FlaskForm):
    """Formulaire de personalisation du dashboard
    """
    plots = SelectMultipleField('Graphiques')
>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
