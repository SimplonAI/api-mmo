from dataclasses import dataclass
from pandas.core.frame import DataFrame
from app.database.db import db

@dataclass
class House(db.Model):
    __tablename__ = "house"
    id = db.Column("ho_id", db.Integer, primary_key=True)
    longitude = db.Column("ho_longitude", db.Numeric(5, 2), nullable=False)
    latitude = db.Column("ho_latitude", db.Numeric(5, 2), nullable=False)
    housing_median_age = db.Column("ho_housing_median_age", db.Integer, nullable=False)
    total_rooms = db.Column("ho_total_rooms", db.Integer, nullable=False)
    total_bedrooms = db.Column("ho_total_bedrooms", db.Integer, nullable=False)
    population = db.Column("ho_population", db.Integer, nullable=False)
    households = db.Column("ho_households", db.Integer, nullable=False)
    median_income = db.Column("ho_median_income", db.Numeric(6, 4), nullable=False)
    median_house_value = db.Column("ho_median_house_value", db.Integer, nullable=False)
    ocean_proximity = db.Column("ho_ocean_proximity", db.String(10), nullable=False)
    created_date = db.Column("ho_created_date", db.DateTime, server_default=db.func.now(), nullable=False)

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
class User(db.Model):
    __tablename__ = "user"
    id = db.Column("u_id", db.Integer, primary_key=True)
    mail = db.Column("u_email", db.String(60), nullable=False)
    password = db.Column("u_password", db.String(128), nullable=False)

@dataclass
class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column("role_id", db.Integer, primary_key=True)
    name = db.Column("role_name", db.String(64), nullable=False)
    permissions = db.Column("role_permissions", db.PickleType, nullable=False)
    users = db.relationship("User", backref="role")

@dataclass
class ModelParams(db.Model):
    __tablename__ = "model_param"
    id = db.Column("mp_id", db.Integer, primary_key=True)
    alpha = db.Column("mp_alpha", db.Numeric(6,5), nullable=False)
    l1_ratio = db.Column("mp_l1_ratio", db.Numeric(6,5), nullable=False)
    max_iter = db.Column("mp_max_iter", db.Integer, nullable=False)
    active = db.Column("mp_active", db.Boolean, default=False, nullable=False)
    created_date = db.Column("ho_created_date", db.DateTime, server_default=db.func.now(), nullable=False)

