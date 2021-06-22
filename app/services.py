from flask_login import LoginManager
from flask import url_for, redirect
from app.models import User

login_manager = LoginManager()


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id) -> User:
    return User.query.get(user_id)

login_manager.login_view = "main.login"