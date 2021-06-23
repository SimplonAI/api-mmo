from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin

from app.forms import LoginForm
from app.models import User

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

# On crée une blueprint qui contiendra toutes les routes/controllers pour les urls de haut niveau ("/", "/login", "/logout"; "/predict")
main_blueprint = Blueprint('main', __name__, url_prefix="/")

@main_blueprint.route("/")
@login_required
def index():
    """Controller pour le dashboard
    """
    return "Hello World ! Agile"

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Controller pour la connexion de l'utilisateur
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user: User = User.query.filter_by(email=login_form.email).first()
        if user is not None and check_password_hash(user.password, login_form.password):
            login_user(user)
            next = request.form.get("next")
            if is_safe_url(next):
                return redirect(next)
            return redirect(url_for("main.index"))
        else:
            flash("Le mot de passe ou l'adresse e-mail ne correspond pas à un utilisateur", category="error")
    return render_template("login.html")