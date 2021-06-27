from datetime import datetime
import os
from io import BytesIO

from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    redirect,
    request,
    url_for,
    send_file,
    current_app,
)
from flask.json import jsonify
from flask_login import login_required, current_user
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg

from app.forms import ModelParamsForm
from app.services import plot_manager
from app.db import db
from app.models import House
from app.utils import house_results_to_dataframe
from app.models import House, ModelParams

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

def response_message_api(route, **kwargs):
    if request.content_type and request.content_type.startswith('application/json'):
        return jsonify(kwargs)
    else:
        if "message" in kwargs:
            flash(kwargs["message"], "info")
        else:
            flash(kwargs["error"], "error")
        return redirect(url_for(route))

@api_blueprint.route("/plot/img/<name>", methods=["GET"])
@login_required
def plot_img(name):
    if name in plot_manager:
        last_house = House.query.order_by(House.updated_date.desc()).first()
        timestamp = datetime.timestamp(last_house.updated_date)
        if not os.path.isdir(f"{current_app.instance_path}/cache"):
            os.mkdir(f"{current_app.instance_path}/cache")
        if os.path.isfile(f"{current_app.instance_path}/cache/{name}_{timestamp}.png"):
            return send_file(f"{current_app.instance_path}/cache/{name}_{timestamp}.png", mimetype='image/png')
        houses = pd.read_sql("SELECT * FROM house", db.engine)
        houses = house_results_to_dataframe(houses)
        fig = plot_manager[name].plot(houses)
        png = BytesIO()
        FigureCanvasAgg(fig).print_png(png)
        fig.savefig(f"{current_app.instance_path}/cache/{name}_{timestamp}.png")
        return Response(png.getvalue(), mimetype='image/png')
    abort(404)

@api_blueprint.route("/plot/json/<name>", methods=["GET"])
@login_required
def plot_json(name):
    if name in plot_manager:
        last_house = House.query.order_by(House.updated_date.desc()).first()
        timestamp = datetime.timestamp(last_house.updated_date)
        if os.path.isfile(f"/cache/{name}_{timestamp}.json"):
            return send_file(f"/cache/{name}_{timestamp}.json")
        houses = pd.read_sql("SELECT * FROM house", db.engine)
        houses = house_results_to_dataframe(houses)

        return Response(plot_manager[name].make_plot_json(houses), mimetype="application/json")
    abort(404)


@api_blueprint.route("/list_houses/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_house(id):
    house = House.query.get_or_404(id)
    db.session.delete(house)
    db.session.commit()
    flash("Vous avez supprimé avec succès la maison !", "info")

    # redirect to the list_house page
    return redirect(url_for("main.list_houses"))

@api_blueprint.route("/model/delete")
@login_required
def delete_model():
    id = request.args.get("id", "")
    if not current_user.has_permissions(["admin.update"]):
        abort(404)
    if id == "":
        return response_message_api("admin.show_model", error="Id manquant", ok=False)
    mp = ModelParams.query.get(id)
    if mp is None:
        return response_message_api("admin.show_model", error="Paramètres du modèle inexistant", ok=False)
    if mp.active:
        return response_message_api("admin.show_model", error="Impossible de supprimer les paramètres actifs.", ok=False)
    nb_mp = ModelParams.query.count()
    if nb_mp == 1:
        return response_message_api("admin.show_model", error="Impossible de supprimer les paramètres, ce sont les derniers paramètres dans la BDD", ok=False)
    db.session.delete(mp)
    db.session.commit()
    return response_message_api("admin.show_model", message="Paramètres supprimés avec succés", ok=True)

@api_blueprint.route("/model/add")
@login_required
def add_model():
    if not current_user.has_permissions(["admin.write"]):
        abort(404)
    model_form = ModelParamsForm()
    if not model_form.validate_on_submit():
        return response_message_api("admin.show_model", error="Le formulaire a été envoyé incorrectement", ok=False)
    mp = ModelParams.query.filter_by(alpha=model_form.alpha.data, l1_ratio=model_form.l1_ratio.data, max_iter=model_form.max_iter.data).first()
    if mp is not None:
        ModelParams.query.filter_by(active=True).update(dict(active=False))
        mp.active = True
        mp.updated_at = datetime.now()
        db.session.commit()
        return response_message_api("admin.show_model", message="Un model possédant les mêmes paramètres était présent, il a été mis par défaut")
    mp = ModelParams(alpha=model_form.alpha.data,l1_ratio=model_form.l1_ratio.data, max_iter=model_form.max_iter.data, active=True)
    db.session.add(mp)
    db.session.commit()
    return response_message_api("admin.show_model", message="Le model a été ajouté et mis par défaut")
