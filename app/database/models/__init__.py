from dataclasses import dataclass
from pandas.core.frame import DataFrame
from app.database.db import db

@dataclass
class House(db.Model):
    __tablename__ = "house"
    id = db.Column("ho_id", db.Integer, primary_key=True)
    longitude = db.Column("ho_longitude", db.Numeric(5, 2))
    latitude = db.Column("ho_latitude", db.Numeric(5, 2))
    housing_median_age = db.Column("ho_housing_median_age", db.Integer)
    total_rooms = db.Column("ho_total_rooms", db.Integer)
    total_bedrooms = db.Column("ho_total_bedrooms", db.Integer)
    population = db.Column("ho_population", db.Integer)
    households = db.Column("ho_households", db.Integer)
    median_income = db.Column("ho_median_income", db.Numeric(6, 4))
    median_house_value = db.Column("ho_median_house_value", db.Integer)
    ocean_proximity = db.Column("ho_ocean_proximity", db.String(10))
    created_date = db.Column("ho_created_date", db.DateTime)

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
class Utilisateur(db.Model):
    __tablename__ = "utilisateur"
    id = db.Column("ut_id", db.Integer, primary_key=True)
    mail = db.Column("ut_mail", db.String(60))
    password = db.Column("ut_password", db.String(128))
