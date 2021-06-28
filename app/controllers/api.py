from app.regression_model import RegressionModel
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
from app.plots import ResidualFittedPlot
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


@api_blueprint.route("/list_houses/delete/<int:id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_house(id):
    house = House.query.get(id)
    if house is None:
        return response_message_api("main.list_houses", error="La maison n'existe pas", ok=False)
    db.session.delete(house)
    db.session.commit()

    # redirect to the list_house page
    return response_message_api("main.list_houses", message="Vous avez supprimé avec succès la maison !", ok=True)

@api_blueprint.route("/model/delete", methods=["POST", "DELETE"])
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

@api_blueprint.route("/model/add", methods=["POST", "PUT"])
@login_required
def add_model():
    if not current_user.has_permissions(["admin.write"]):
        abort(404)
    model_form = ModelParamsForm()
    if not model_form.validate_on_submit():
        return response_message_api("admin.show_model", error="Le formulaire a été envoyé incorrectement", ok=False)
    mp = ModelParams.query.filter_by(alpha=model_form.alpha.data, l1_ratio=model_form.l1_ratio.data, max_iter=model_form.max_iter.data).first()
    ModelParams.query.filter_by(active=True).update(dict(active=False))
    db.session.commit()
    if mp is not None:
        mp.active = True
        mp.updated_at = datetime.now()
        db.session.commit()
        return response_message_api("admin.show_model", message="Un model possédant les mêmes paramètres était présent, il a été mis par défaut", ok=True)
    mp = ModelParams(alpha=model_form.alpha.data,l1_ratio=model_form.l1_ratio.data, max_iter=model_form.max_iter.data, active=True)
    db.session.add(mp)
    db.session.commit()
    return response_message_api("admin.show_model", message="Le model a été ajouté et mis par défaut", ok=True)

@api_blueprint.route("/model/list")
@login_required
def list_model():
    if not current_user.has_permissions(["admin.read"]):
        abort(403)
    params = ModelParams.query.all()
    return jsonify(dict(ok=True, data=[param.to_dict() for param in params]))

@api_blueprint.route("/house/list")
@login_required
def list_house():
    try:
        items_per_page = int(request.args.get("per_page", "25")) 
        page = int(request.args.get("p", "1"))
    except ValueError:
        abort(400)
    houses = House.query.limit(items_per_page).offset(items_per_page * (page - 1)).all()
    if houses is None:
        return jsonify(dict(ok=True, data=[]))
    return jsonify(dict(ok=True, data=[house.to_dict() for house in houses]))

@api_blueprint.route("/resid-plot")
@login_required
def resid_plot():
    if not current_user.has_permissions(["admin.read"]):
        abort(403)
    try:
        alpha = float(request.args.get("alpha", ""))
        l1_ratio = float(request.args.get("l1_ratio", ""))
        max_iter = float(request.args.get("max_iter", ""))
    except ValueError:
        abort(400)
    mp = ModelParams(alpha=alpha, l1_ratio=l1_ratio, max_iter=max_iter)
    data = house_results_to_dataframe(pd.read_sql("SELECT * FROM house", db.engine))
    reg_model = RegressionModel(data, mp)
    res_plot = ResidualFittedPlot("Residual / Fitted Plot", reg_model.predict(data, reg_model.x_test), reg_model.y_test, "House Median Value", "res_plot", reg_model)
    if "json" in request.args:
        return Response(res_plot.make_plot_json(data), mimetype="application/json")
    last_house = House.query.order_by(House.updated_date.desc()).first()
    timestamp = datetime.timestamp(last_house.updated_date)
    if not os.path.isdir(f"{current_app.instance_path}/cache"):
        os.mkdir(f"{current_app.instance_path}/cache")
    if os.path.isfile(f"{current_app.instance_path}/cache/resid_plot_{mp.to_hash()}_{timestamp}.png"):
        return send_file(f"{current_app.instance_path}/cache/resid_plot_{mp.to_hash()}_{timestamp}.png", mimetype='image/png')
    fig = res_plot.plot(data)
    png = BytesIO()
    FigureCanvasAgg(fig).print_png(png)
    return Response(png.getvalue(), mimetype='image/png')
