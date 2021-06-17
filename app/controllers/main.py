from flask import Blueprint

main_controller = Blueprint('main', __name__, url_prefix="/")

@main_controller.route("/")
def index():
    return "Hello World ! Agile"