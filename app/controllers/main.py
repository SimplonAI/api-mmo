from flask import Blueprint, render_template
from flask_login import login_required

main_controller = Blueprint('main', __name__, url_prefix="/")

@main_controller.route("/")
@login_required
def index():
    return "Hello World ! Agile"

@main_controller.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")