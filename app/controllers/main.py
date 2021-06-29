from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user
from flask_login.utils import logout_user
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin
import math

from werkzeug.utils import send_file
from app.models import User, House
from app.forms import DashboardForm, LoginForm, PredictForm, HouseForm
from app.services import plot_manager
from app.utils import prediction, get_location
from flask import Flask,render_template
import pandas as pd
import seaborn as sns
import io 
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from app.db import db

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


# On crée une blueprint qui contiendra toutes les routes/controllers pour les urls de haut niveau ("/", "/login", "/logout"; "/predict")
main_blueprint = Blueprint("main", __name__, url_prefix="/")


@main_blueprint.route("/")
@login_required
def index():
    """Controller pour le dashboard"""
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
    """Controller pour la connexion de l'utilisateur"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user: User = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and check_password_hash(
            user.password, login_form.password.data
        ):
            login_user(user, remember=login_form.remember_me.data)
            next = request.args.get("next")
            if next is not None and is_safe_url(next):
                return redirect(next)
            return redirect(url_for("main.index"))
        else:
            flash(
                "Le mot de passe ou l'adresse e-mail ne correspond pas à un utilisateur",
                category="error",
            )
    return render_template("login.html", login_form=login_form)


@main_blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Controller pour déconnecter un utilisateur"""
    logout_user()
    return redirect(url_for("main.login"))


@main_blueprint.route("/estimation", methods=["GET", "POST"])
@login_required
def estimation():
    """Controller pour l'affichage de l'estimation"""

    predict_form = PredictForm()
    r_score, y = None, None
    if predict_form.validate_on_submit():
        r_score, y = prediction(predict_form)

    return render_template(
        "predict.html", predict_form=predict_form, r_score=r_score, y=y
    )


@main_blueprint.route("/list_houses", methods=["GET", "POST"])
@login_required
def list_houses():
    """Controller pour afficher la liste des logements"""
    page = request.args.get("p", 1)
    try:
        page = int(page)
    except ValueError:
        page = 1

    count_house = House.query.count()
    pages_shown = 9
    items_per_page = 25
    max_pages = math.ceil(float(count_house) / float(items_per_page))
    start_page = 1
    if page > pages_shown/2:
        start_page = (int(min((float(page)+math.floor(float(pages_shown)/2)), max_pages)) - pages_shown + 1)

    if start_page < 1:
        start_page = 1

    end_page = (start_page + pages_shown - 1)
    if end_page > int(max_pages):
        end_page = int(max_pages)

    list_housing = House.query.limit(items_per_page).offset(items_per_page * (page - 1)).all()

    return render_template(
        "list_houses.html",
        list_housing=list_housing,
        count_page=max_pages,
        current_page=page,
        start_page=start_page,
        end_page=end_page,
        title="list_housing",
    )

@main_blueprint.route("/add_house", methods=["GET", "POST"])
@login_required
def add_house():
    """Controller pour ajouter un logements"""
    house_form = HouseForm()
    if house_form.validate_on_submit():

        lat, lng = get_location(house_form)

        insert_house = House(
            longitude=round(lng, 2),
            latitude=round(lat, 2),
            housing_median_age=house_form.median_age.data,
            total_rooms=house_form.total_rooms.data,
            total_bedrooms=house_form.total_bedrooms.data,
            population=house_form.population.data,
            households=house_form.households.data,
            median_income=house_form.median_income.data,
            median_house_value=house_form.median_house_value.data,
            ocean_proximity=house_form.ocean_proximity.data,
        )
        # On l'ajoute à la BDD
        db.session.add(insert_house)
        # On confirme les changements de la transaction
        db.session.commit()

        flash("Le formulaire est bien rempli success", category="info")
        return redirect(url_for("main.list_houses"))

    elif len(house_form.errors) > 0:
        flash("Le formulaire n'est pas bien rempli", category="error")
    return render_template("add_house.html", house_form=house_form)



    
 
# ici on récupère l'ID de la maison , dont la vignette a été cliquée, via le chemin "/house/house_id"
@main_blueprint.route("/house/<house_id>", methods=["GET"])
@login_required
def info_house(house_id):

# renvoie une erreur 404 si aucune id de maison n'a été relevé dans la requête vers le serveur

    House_=House.query.filter_by(id=house_id).first_or_404()
    
    return render_template("info_house.html",
                           house_=House_,
                            title="info_house" 
                            )

@main_blueprint.route("/faq")
@login_required
def faq():
    return render_template("faq.html")