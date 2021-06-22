from operator import index
from pandas.core.frame import DataFrame
from pandas._testing import assert_frame_equal
from app.utils import format_data_housing, house_results_to_dataframe
import pytest
import pandas as pd
from app import create_app
from app.db import db
from app.models import House, User, UserRole, ModelParams

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SERVER_NAME": "exemple.com",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test"
    })
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    db.create_all()
    yield client

def test_db_schema(client):
    """Check if tables have successfully been added to the db
    """
    table_names = ["user", "house", "user_role", "model_param"]
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
    houses = house_results_to_dataframe(houses)
    assert_frame_equal(houses, data, check_dtype=False)
