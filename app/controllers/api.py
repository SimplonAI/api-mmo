from io import BytesIO
from flask import Blueprint, Response, abort, abort, flash, redirect, render_template, url_for

from flask_login import login_required
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from app.forms import DashboardForm
from app.services import plot_manager
from app.db import db
from app.utils import house_results_to_dataframe
from app.models import House
api_blueprint = Blueprint('api', __name__, url_prefix="/api")


@api_blueprint.route("/plot/<name>", methods=["GET"])
@login_required
def plot(name):
    if name in plot_manager:
        houses = pd.read_sql("SELECT * FROM house", db.engine)
        houses = house_results_to_dataframe(houses)
        fig = plot_manager[name].plot(houses)
        png = BytesIO()
        FigureCanvasAgg(fig).print_png(png)
        return Response(png.getvalue(), mimetype='image/png')
    abort(404)


@api_blueprint.route("/list_houses/delete/<int:id>", methods=["GET","POST"])
@login_required
def delete_house():
    house = House.query.get_or_404(id)
    db.session.delete(house)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('list_houses'))


    return render_template(title="Delete Department")
