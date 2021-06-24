from flask_login import UserMixin
from dataclasses import dataclass
from pandas.core.frame import DataFrame
import urllib, hashlib
from app.db import db
from sqlalchemy.sql import func

@dataclass
class House(db.Model):
    """Table House de la BDD, il est possible de faire des requetes sql 
    avec House.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "house"
    id = db.Column("ho_id", db.Integer, primary_key=True)
    longitude = db.Column("ho_longitude", db.Numeric(5, 2), nullable=False)
    latitude = db.Column("ho_latitude", db.Numeric(5, 2), nullable=False)
    housing_median_age = db.Column("ho_housing_median_age", db.Integer, nullable=False)
    total_rooms = db.Column("ho_total_rooms", db.Integer, nullable=False)
    total_bedrooms = db.Column("ho_total_bedrooms", db.Integer, nullable=True)
    population = db.Column("ho_population", db.Integer, nullable=False)
    households = db.Column("ho_households", db.Integer, nullable=False)
    median_income = db.Column("ho_median_income", db.Numeric(6, 4), nullable=False)
    median_house_value = db.Column("ho_median_house_value", db.Integer, nullable=False)
    ocean_proximity = db.Column("ho_ocean_proximity", db.String(10), nullable=False)
    created_date = db.Column("ho_created_date", db.DateTime, server_default=func.now(), nullable=False)
    updated_date = db.Column("ho_updated_date", db.DateTime, server_default=func.now(), nullable=False)

    def insert_from_pd(data_housing: DataFrame):
        data_housing = data_housing.rename(
            columns={
                "longitude": "ho_longitude",
                "latitude": "ho_latitude",
                "housing_median_age": "ho_housing_median_age",
                "total_rooms": "ho_total_rooms",
                "total_bedrooms": "ho_total_bedrooms",
                "population": "ho_population",
                "households": "ho_households",
                "median_income": "ho_median_income",
                "median_house_value": "ho_median_house_value",
                "ocean_proximity": "ho_ocean_proximity",
            }
        )
        data_housing.index += 1
        data_housing.rename_axis(index="ho_id")
        data_housing.to_sql("house", if_exists="append", con=db.engine, index=False)

@dataclass
class User(UserMixin, db.Model):
    """Table User de la BDD, il est possible de faire des requetes sql 
    avec User.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "user"
    id = db.Column("u_id", db.Integer, primary_key=True)
    email = db.Column("u_email", db.String(60), nullable=False)
    password = db.Column("u_password", db.String(128), nullable=False)
    role_id = db.Column("u_role_id", db.ForeignKey("user_role.role_id"))

    def get_avatar(self):
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() + "?"
        gravatar_url += urllib.parse.urlencode({'s':"40"})
        return gravatar_url

@dataclass
class UserRole(db.Model):
    """Table UserRole de la BDD, il est possible de faire des requetes sql 
    avec UserRole.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "user_role"
    id = db.Column("role_id", db.Integer, primary_key=True)
    name = db.Column("role_name", db.String(64), nullable=False)
    permissions = db.Column("role_permissions", db.PickleType, nullable=False)
    users = db.relationship("User", backref="role")

@dataclass
class ModelParams(db.Model):
    """Table ModelParams de la BDD, il est possible de faire des requetes sql 
    avec ModelParams.query (voir la doc de flask-sqlalchemy)
    """
    __tablename__ = "model_param"
    id = db.Column("mp_id", db.Integer, primary_key=True)
    alpha = db.Column("mp_alpha", db.Numeric(6,5), nullable=False)
    l1_ratio = db.Column("mp_l1_ratio", db.Numeric(6,5), nullable=False)
    max_iter = db.Column("mp_max_iter", db.Integer, nullable=False)
    active = db.Column("mp_active", db.Boolean, default=False, nullable=False)
    created_date = db.Column("ho_created_date", db.DateTime, server_default=func.now(), nullable=False)

