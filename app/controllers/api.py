from io import BytesIO
from flask import Blueprint, Response, abort, send_file, current_app
from flask.json import jsonify
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from datetime import datetime
import os
import plotly
import plotly.graph_objs as go
import json

from app.forms import DashboardForm
from app.services import plot_manager
from app.db import db
from app.models import House
from app.utils import house_results_to_dataframe

api_blueprint = Blueprint('api', __name__, url_prefix="/api")

@api_blueprint.route("/plot/img/<name>", methods=["GET"])
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
