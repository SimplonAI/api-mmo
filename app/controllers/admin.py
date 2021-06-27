from flask import Blueprint
from flask.templating import render_template
from flask_login import login_required
from flask_sqlalchemy.model import Model
from app.controllers.middlewares import has_permissions
from app.forms import ModelParamsForm
from app.models import ModelParams

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

admin_blueprint.before_request(login_required(has_permissions("admin.read")))

@admin_blueprint.route("/show-model")
def show_model():
    model_form = ModelParamsForm()
    mp: ModelParams = ModelParams.query.filter_by(active = True).first()
    all_params = ModelParams.query.all()
    # Utilisé seulement si l'utilisateur n'a pas JS activé
    if model_form.validate_on_submit():
        mp = model_form
    elif mp is not None:
        model_form.alpha.data = mp.alpha
        model_form.l1_ratio.data = mp.l1_ratio
        model_form.max_iter.data = mp.max_iter
    return render_template("show_model.html", mp=mp, all_params=all_params, form=model_form)

@admin_blueprint.route("/model/<id>/edit")
def edit_model(id):
    return id