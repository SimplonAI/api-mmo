from operator import index
from pandas.core.frame import DataFrame
from pandas._testing import assert_frame_equal
from app.utils import format_data_housing
import pytest
import pandas as pd
from flask import jsonify
from app import create_app
from app.database.db import db
from app.database.models import House, Utilisateur
from app.db_commands import insert_db

@pytest.fixture
def client():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'example.com'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    db.create_all()
    yield client

def test_db_schema(client):
    """Check if tables have successfully been added to the db
    """
    table_names = ["utilisateur", "house"]
    with db.engine.connect() as connexion:
        for table_name in table_names:
            assert db.engine.dialect.has_table(connexion, table_name) == True    

def test_inserted_data(client):
    """Check if insert-db command inserts correctly all the data
    """
    data = pd.read_csv("housing.csv")
    data = format_data_housing(data)
    House.insert_from_pd(data)
    houses: DataFrame = pd.read_sql("SELECT * FROM house", db.engine)
    assert len(houses) == data.shape[0]
    houses.drop(columns=["ho_id", "ho_created_date"], inplace=True)
    houses = houses.rename(
        columns={
            "ho_longitude": "longitude",
            "ho_latitude": "latitude",
            "ho_housing_median_age": "housing_median_age",
            "ho_total_rooms": "total_rooms",
            "ho_total_bedrooms": "total_bedrooms",
            "ho_population": "population",
            "ho_households": "households",
            "ho_median_income": "median_income",
            "ho_median_house_value": "median_house_value",
            "ho_ocean_proximity": "ocean_proximity",
        }
    )
    assert_frame_equal(houses, data)
