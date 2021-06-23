from re import I
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user
from flask_login.utils import logout_user
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin

from app.forms import DashboardForm, LoginForm
from app.models import User
from app.services import plot_manager

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
    plots = plot_manager.defaults
    dashboard_form = DashboardForm()
    dashboard_form.plots.choices = plot_manager.available_plots
    if request.method == "POST" and dashboard_form.validate_on_submit():
            if dashboard_form.plots.data is not None and len(dashboard_form.plots.data) > 0:
                plots = dashboard_form.plots.data
    else:
        dashboard_form.plots.data = plots
    return render_template("dashboard.html", plots=plots, dashboard_form=dashboard_form)

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Controller pour la connexion de l'utilisateur
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user: User = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            next = request.args.get("next")
            if next is not None and is_safe_url(next):
                return redirect(next)
            return redirect(url_for("main.index"))
        else:
            flash("Le mot de passe ou l'adresse e-mail ne correspond pas à un utilisateur", category="error")
    return render_template("login.html", login_form=login_form)

@main_blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Controller pour déconnecter un utilisateur
    """
    logout_user()
    return redirect(url_for("main.login"))
