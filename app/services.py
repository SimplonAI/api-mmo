from app.plots import PlotManager, ScatterPlot
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

plot_manager.defaults = ["median_price_income"]