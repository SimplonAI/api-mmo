from math import pi
import os
import joblib
from flask import current_app
import numpy as np
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

from app.models import ModelParams

class SavedModel():
    def __init__(self, model, x_train, x_test, y_train, y_test, params) -> None:
        self.model = model
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.params = params

class RegressionModel():
    def __init__(self, data: pd.DataFrame, params: ModelParams) -> None:
        self.params = params
        if not os.path.isdir(f"{current_app.instance_path}/cache"):
            os.mkdir(f"{current_app.instance_path}/cache")
        if not os.path.isdir(f"{current_app.instance_path}/cache/regression"):
            os.mkdir(f"{current_app.instance_path}/cache/regression")
        if os.path.isfile(self.save_path):
            self.__saved_model: SavedModel = joblib.load(self.save_path)
        else:
            self.build_model(data)

    @property
    def save_path(self):
        return f"{current_app.instance_path}/cache/regression/model_{self.params.to_hash()}.sav"

    @property
    def model(self):
        return self.__saved_model.model

    @property
    def x_train(self):
        return self.__saved_model.x_train
    
    @property
    def y_train(self):
        return self.__saved_model.y_train

    @property
    def x_test(self):
        return self.__saved_model.x_test
    
    @property
    def y_test(self):
        return self.__saved_model.y_test

    def save_model(self):
        joblib.dump(self.__saved_model, self.save_path)

    def get_pipeline(self, data: pd.DataFrame):
        housing_num = data.drop(["median_house_value", "ocean_proximity"], axis=1)
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

        return ColumnTransformer(
            [
                ("num", num_pipeline, num_attribs),
                ("cat", OneHotEncoder(), cat_attribs),
            ]
        )

    def build_model(self, data: pd.DataFrame):
        pipeline = self.get_pipeline(data)

        data_no_island = data[data["ocean_proximity"] != "ISLAND"]
        x = data_no_island.drop("median_house_value", axis=1)
        y = data_no_island["median_house_value"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.33, random_state=1
        )

        housing_prepared = pipeline.fit_transform(x_train)
        sgd = SGDRegressor(
            l1_ratio=self.params.l1_ratio,
            alpha=self.params.alpha,
            max_iter=self.params.max_iter,
            penalty="elasticnet",
        )
        sgd.fit(housing_prepared, y_train)
        self.__saved_model = SavedModel(sgd, x_train, x_test, y_train, y_test, self.params)
        self.save_model()

    def retrain(self, data):
        """Permet de réentraîner le même modèle sur un nouveau dataset

        Args:
            data (pd.DataFrame): DataFrame sur lequel entraîné de nouveau le modèle
        """
        pipeline = self.get_pipeline(data)

        housing_prepared = pipeline.fit_transform(self.__saved_model.x_train)
        sgd = SGDRegressor(
            l1_ratio=self.params.l1_ratio,
            alpha=self.params.alpha,
            max_iter=self.params.max_iter,
            penalty="elasticnet",
        )
        sgd.fit(housing_prepared, self.__saved_model.y_train)
        self.__saved_model = SavedModel(sgd, self.__saved_model.x_train, self.__saved_model.x_test, self.__saved_model.y_train, self.__saved_model.y_test, self.params)
        self.save_model()

    
    def r_score(self, data):
        """Le score R² pour le model entraîné

        Args:
            data (pd.DataFrame): DataFrame contenant toutes les données du modèle entraîné

        Returns:
            float: Le score R² calculé
        """
        pipeline = self.get_pipeline(data)

        housing_test_no_island = pipeline.fit_transform(self.__saved_model.x_test)
        # Calcul du r score
        return self.model.score(housing_test_no_island, self.__saved_model.y_test)

    def rmse(self, data):
        """Retourne le root mean squared error du model entraîné

        Args:
            data (pd.DataFrame): Dataframe contenant toutes les valeurs du modèle entraîné

        Returns:
            float: Le root mean squared error calculé
        """
        pipeline = self.get_pipeline(data)

        housing_test_no_island = pipeline.fit_transform(self.__saved_model.x_test)
        y_pred = self.model.predict(housing_test_no_island)
        return np.sqrt(mean_squared_error(self.__saved_model.y_test, y_pred))

    def self_predict(self, data):
        """Permet de retourner les valeurs prédites sur les données d'entraînements
        """
        pipeline = self.get_pipeline(data)
        housing_value = pipeline.fit_transform(self.__saved_model.x_train)
        return self.model.predict(housing_value)

    def predict(self, data, x_value):
        """Permer de prédire des valeurs sur des données de tests ou de validation

        Args:
            data (pd.DataFrame): DataFrame contenant toutes les valeurs des données d'entraînements
            x_value (pd.Series): Series contenant les valeurs à prédire

        Returns:
            list: Liste de valeurs prédites pour x_value
        """
        pipeline = self.get_pipeline(data)
        pipeline.fit_transform(self.__saved_model.x_train)
        housing_value = pipeline.transform(x_value)
        return self.model.predict(housing_value)