<<<<<<< HEAD
from app.plots import DistPlot, GeoPlots, PlotManager, ScatterPlot
=======
from app.plots import PlotManager, ScatterPlot
>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id) -> User:
    return User.query.get(user_id)


# Défini sur quelle route rediriger lorsqu'une route protégé par login_required est atteinte par un utilisateur non connecté
login_manager.login_view = "main.login"

plot_manager = PlotManager()
plot_manager.add_plot(ScatterPlot("Prix Médian en fonction du revenu médian", "median_income", "median_house_value", "Revenue médian", "Prix médian", key="median_price_income"))
<<<<<<< HEAD
plot_manager.add_plot(GeoPlots("Prix médian selon la longitude et la latitude", hue="median_house_value", key="long_lat_price_map"))
plot_manager.add_plot(DistPlot("Distribution des revenus médians", "median_income", key="median_income_dist"))
plot_manager.add_plot(DistPlot("Distribution des prix médians", "median_house_value", key="median_house_value_dist"))
plot_manager.add_plot(DistPlot("Distribution de la population dans les block", "population", key="population_dist", bins=50))
plot_manager.add_plot(DistPlot("Distribution de la proximité à l'océan", "ocean_proximity", "count", key="ocean_proximity_dist"))

plot_manager.add_plot(ScatterPlot("Population en fonction du revenu médian", "median_income", "population", "Revenue médian", "Population", key="popu_income_scat"))
plot_manager.add_plot(ScatterPlot("Nombre de pièces en fonction de la population", "population", "total_rooms", "Population", "Nombre de pièces", key="rooms_income_scat"))

plot_manager.defaults = ["median_price_income", "long_lat_price_map", "ocean_proximity_dist", "median_income_dist", "median_house_value_dist", "population_dist"]
=======

plot_manager.defaults = ["median_price_income"]
>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
