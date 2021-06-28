from os import pipe
from app.forms import PredictForm
import pandas as pd
from flask import current_app
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

from app.models import ModelParams
from app.db import db
import requests
import json

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

def get_location(predict_form: PredictForm):
    api_key = current_app.config.get("MAPQUEST_KEY")
    if api_key is None:
        current_app.logger.error("La clé API pour Mapquest n'est pas configuré (MAPQUEST_KEY)")
    parameters = {
        "key": api_key,
        "location": f"{predict_form.adresse.data}, {predict_form.ville.data}, {predict_form.etat.data} {predict_form.code_postal.data}"
    }

    response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params = parameters)
    location = json.loads(response.text)["results"]
    lat = location[0]['locations'][0]['latLng']['lat']
    lng = location[0]['locations'][0]['latLng']['lng']
    return lat, lng



def prediction(predict_form: PredictForm):
    """Prédit la valeur médiane d'une maison
    """
    # On récupère les paramètres de modélisation actifs
    mp = ModelParams.query.filter_by(active=True).first()
    # Si aucun paramètres dans la BDD, on quitte la fonction
    if mp is None:
        return
    
    # On récupère toutes les maisons de la BDD via pandas
    data = pd.read_sql("SELECT * FROM house", db.engine)
    # On renomme les colonnes du dataframe pour correspondre à ceux du csv
    data = house_results_to_dataframe(data)

    # Variable nécessaire pour créer le menu de sélection
    """ déplacé dans forms.py
    """
    lat, lng = get_location(predict_form)

    # On demande les données nécessaire à la prédiction puis on les stock dans un dictionnaire
    d_test = {
                "longitude": [lng],
                "latitude": [lat],
                "housing_median_age": [predict_form.median_age.data],
                "total_rooms": [predict_form.total_rooms.data],
                "total_bedrooms": [predict_form.total_bedrooms.data],
                "population": [predict_form.population.data],
                "households": [predict_form.households.data],
                "median_income": [predict_form.median_income.data],
                "ocean_proximity": [predict_form.ocean_proximity.data],
            }
    
    # On prédit le prix
    r_score, y, _ = regression(data, pd.DataFrame.from_dict(d_test), mp)
    
    return r_score, y



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
