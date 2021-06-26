from flask import Blueprint
from flask.templating import render_template
from flask_login import login_required
from app.controllers.middlewares import has_permissions

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

admin_blueprint.before_request(login_required(has_permissions("admin.read")))

@admin_blueprint.route("/show-model")
def show_model():
    return render_template("show_model.html")