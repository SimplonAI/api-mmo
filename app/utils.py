import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import SGDRegressor, LinearRegression, Ridge
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
)
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import numpy as np


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
    data_housing.drop(columns=["ho_id", "ho_created_date"], inplace=True)
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


def regression(data, x_test, y_true=None, params=None):
    X = data.drop("median_house_value", axis=1)
    housing_num = X.drop(["ocean_proximity"], axis=1)

    col_names = "total_rooms", "total_bedrooms", "population", "households"
    rooms_ix, bedrooms_ix, population_ix, households_ix = [
        data.columns.get_loc(c) for c in col_names
    ]

    class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
        def __init__(self, add_bedrooms_per_room=True):
            self.add_bedrooms_per_room = add_bedrooms_per_room

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
            population_per_household = X[:, population_ix] / X[:, households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
                return np.c_[
                    X, rooms_per_household, population_per_household, bedrooms_per_room
                ]
            else:
                return np.c_[X, rooms_per_household, population_per_household]

    num_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("attribs_adder", CombinedAttributesAdder()),
            ("std_scaler", StandardScaler()),
        ]
    )

    num_attribs = list(housing_num)
    cat_attribs = ["ocean_proximity"]

    full_pipeline = ColumnTransformer(
        [
            ("num", num_pipeline, num_attribs),
            ("cat", OneHotEncoder(), cat_attribs),
        ]
    )

    data_no_island = data[data["ocean_proximity"] != "ISLAND"]
    X_noisland = data_no_island.drop("median_house_value", axis=1)
    y_no_island = data_no_island["median_house_value"]

    X_train_no_island, _, y_train_no_island, _ = train_test_split(
        X_noisland, y_no_island, test_size=0.33, random_state=1
    )

    housing_prepared_no_island = full_pipeline.fit_transform(X_train_no_island)

    sgd = SGDRegressor(
        l1_ratio=params.l1_ratio,
        alpha=params.alpha,
        max_iter=params.max_iter,
        penalty="elasticnet",
    )
    sgd.fit(housing_prepared_no_island, y_train_no_island)

    r_score = sgd.score(housing_prepared_no_island, y_train_no_island)
    housing_valid_no_island = full_pipeline.transform(x_test)
    y_pred = sgd.predict(housing_valid_no_island)
    
    if y_true is not None:
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return r_score, y_pred, rmse

    return r_score, y_pred, None