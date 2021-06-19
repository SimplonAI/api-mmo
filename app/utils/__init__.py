import pandas as pd


def format_data_housing(data_housing: pd.DataFrame):
    data_housing["total_bedrooms"] = data_housing["total_bedrooms"].fillna(
        data_housing["total_bedrooms"].median()
    )
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
        'int64'
    )
    return data_housing