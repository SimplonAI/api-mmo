from flask import Blueprint, render_template
from flask_login import login_required

# On crée une blueprint qui contiendra toutes les routes/controllers pour les urls de haut niveau ("/", "/login", "/logout"; "/predict")
main_blueprint = Blueprint('main', __name__, url_prefix="/")

@main_blueprint.route("/")
@login_required
def index():
    """Controller pour le dashboard
    """
    return render_template("dashboard.html")

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Controller pour la connexion de l'utilisateur
    """
    return render_template("login.html")