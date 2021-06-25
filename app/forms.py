from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

# Chaque formulaire hérite de Flask-WTF afin de gérer plus facilement la validation des données et la génération des champs HTML

class LoginForm(FlaskForm):
    """Formulaire de connexion
    """
    email = EmailField('Adresse e-mail', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')

class DashboardForm(FlaskForm):
    """Formulaire de personalisation du dashboard
    """
    plots = SelectMultipleField('Graphiques')


class HouseForm(FlaskForm):
    """Formulaire d'ajout de logement
    """
    email = EmailField('Adresse e-mail', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')

    address = Field
    housing_median_age = 

