from io import BytesIO
from flask import Blueprint, Response, abort, send_file
from flask.json import jsonify
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime
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
        if os.path.isfile(f"/cache/{name}_{timestamp}.png"):
            return send_file(f"/cache/{name}_{timestamp}.png", mimetype='image/png')
        houses = pd.read_sql("SELECT * FROM house", db.engine)
        houses = house_results_to_dataframe(houses)
        fig = plot_manager[name].plot(houses)
        png = BytesIO()
        FigureCanvasAgg(fig).print_png(png)
        fig.savefig()
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

        return jsonify(plot_manager[name].make_plot_json(houses))
    abort(404)
