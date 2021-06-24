from io import BytesIO
from flask import Blueprint, Response, abort
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from app.forms import DashboardForm
from app.services import plot_manager
from app.db import db
from app.utils import house_results_to_dataframe

api_blueprint = Blueprint('api', __name__, url_prefix="/api")

@api_blueprint.route("/plot/<name>", methods=["GET"])
def plot(name):
    if name in plot_manager:
        houses = pd.read_sql("SELECT * FROM house", db.engine)
        houses = house_results_to_dataframe(houses)
        fig = plot_manager[name].plot(houses)
        png = BytesIO()
        FigureCanvasAgg(fig).print_png(png)
        return Response(png.getvalue(), mimetype='image/png')
    abort(404)
