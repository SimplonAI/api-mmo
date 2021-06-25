from os import pipe
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
)
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import numpy as np

from app.regression_model import RegressionModel


def format_data_housing(data_housing: pd.DataFrame):
    """Permet de formatter les champs du dataframe afin de les conformer au type de la BDD

    Args:
        data_housing (pd.DataFrame): dataframe provenant du fichier csv

    Returns:
        pd.DataFrame: Le dataframe converti
    """
    data_housing[
        [
            "population",
            "housing_median_age",
            "total_rooms",
            "total_bedrooms",
            "households",
            "median_house_value",
        ]
    ] = data_housing[
        [
            "population",
            "housing_median_age",
            "total_rooms",
            "total_bedrooms",
            "households",
            "median_house_value",
        ]
    ].astype(
        pd.Int64Dtype()
    )
    return data_housing


def house_results_to_dataframe(data_housing: pd.DataFrame):
    """Transforme un dataframe provenant d'une requete sql en dataframe similaire à celui du fichier csv

    Args:
        data_housing (pd.DataFrame): Le dataframe provenant de la requete sql

    Returns:
        pd.DataFrame: Un dataframe similaire au fichier csv
    """
    # On élimine les colonnes id et created_date du dataframe
    data_housing.drop(columns=["ho_id", "ho_created_date", "ho_updated_date"], inplace=True)
    # On renomme les colonnes
    data_housing = data_housing.rename(
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
    return data_housing


def regression(data, x_valid, params=None):
    regression_model = RegressionModel(data, params)

    # Calcul du r score
    r_score = regression_model.r_score(data)

    # prédiction du prix
    y_pred = regression_model.predict(data, x_valid)
    
    return r_score, y_pred, regression_model.rmse(data)

def convert(o):
    if isinstance(o, np.generic): return o.item()  
    raise TypeError