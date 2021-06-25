from abc import ABCMeta, abstractmethod
from app.utils import convert
import json

import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import geopandas
import contextily as cx
import plotly
import plotly.graph_objs as go
from slugify import slugify


class AbstractPlot(metaclass=ABCMeta):
    def __init__(
        self, name, x=None, y=None, x_label=None, y_label=None, key=None
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.__key = key

    @property
    def slug(self):
        return slugify(self.name) if self.__key is None else self.__key

    @abstractmethod
    def make_plot_img(self, data, ax):
        pass

    @abstractmethod
    def make_plot_json(self, data):
        pass

    def plot(self, data):
        fig, ax = plt.subplots(1)
        self.make_plot_img(data=data, ax=ax)

        ax.set_title(self.name)
        if self.x_label is not None:
            ax.set_xlabel(self.x_label)
        if self.y_label is not None:
            ax.set_ylabel(self.y_label)
        fig.tight_layout()

        return fig


class PlotManager(dict[str, AbstractPlot]):
    def __setitem__(self, k: str, v: AbstractPlot) -> None:
        if not isinstance(v, AbstractPlot):
            raise ValueError("Plot is not an abstractplot child class")
        return super().__setitem__(k, v)

    def add_plot(self, plot: AbstractPlot):
        self[plot.slug] = plot

    @property
    def defaults(self):
        return self.__defaults or []

    @defaults.setter
    def defaults(self, defaults):
        self.__defaults = []
        for default in defaults:
            if default not in self:
                raise ValueError(f"Le plot {default} n'existe pas")
            self.__defaults.append(default)

    @property
    def available_plots(self):
        return [(self[plot].slug, self[plot].name) for plot in self]


class ScatterPlot(AbstractPlot):
    def make_plot_img(self, data, ax):
        sn.scatterplot(self.x, self.y, data=data, ax=ax)

    def make_plot_json(self, data):
        d = [go.Scatter(x=data[self.x], y=data[self.y], mode="markers")]
        return json.dumps(d, cls=plotly.utils.PlotlyJSONEncoder)


class GeoPlots(AbstractPlot):
    def __init__(
        self,
        name,
        x="longitude",
        y="latitude",
        x_label="Longitude",
        y_label="Latitude",
        key=None,
        hue=None,
    ) -> None:
        super().__init__(name, x=x, y=y, x_label=x_label, y_label=y_label, key=key)
        self.hue = hue

    def make_plot_img(self, data, ax):
        gdf = geopandas.GeoDataFrame(
            data, geometry=geopandas.points_from_xy(data[self.x], data[self.y])
        )
        gdf.set_crs(epsg=4326, inplace=True)
        gdf.plot(
            figsize=(15, 15),
            markersize=20,
            column=self.hue,
            legend=True,
            marker=".",
            alpha=0.5,
            ax=ax,
        )
        cx.add_basemap(
            ax, crs=gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik
        )

    def make_plot_json(self, data: pd.DataFrame):
        return json.dumps(
            {
                "data": [
                    {
                        "type": "scattermapbox",
                        "mode": "markers",
                        "text": list(data[self.hue]),
                        "lon": list(data[self.x]),
                        "lat": list(data[self.y]),
                        "marker": {
                            "color": list(data[self.hue]),
                            "colorscale": [
                                [0, "rgb(255,0,0)"],
                                [0.125, "rgb(255, 111, 200)"],
                                [0.25, "rgb(255, 234, 0)"],
                                [0.375, "rgb(151, 255, 0)"],
                                [0.5, "rgb(44, 255, 150)"],
                                [0.625, "rgb(0, 152, 255)"],
                                [0.75, "rgb(0, 25, 255)"],
                                [0.875, "rgb(0, 0, 200)"],
                                [1, "rgb(150,0,90)"],
                            ],
                            "cmin": data[self.hue].min(),
                            "cmax": data[self.hue].max(),
                            "reversescale": True,
                            "opacity": 0.5,
                            "size": 3,
                            "colorbar": {
                                "thickness": 10,
                                "titleside": "right",
                                "outlinecolor": "rgba(68,68,68,0)",
                                "ticks": "outside",
                                "ticklen": 3,
                                "shoticksuffix": "last",
                                "ticksuffix": " Dm€",
                                "dtick": 30000,
                            },
                        },
                        "name": self.name,
                    }
                ],
                "layout": {
                    "title": self.name,
                    "dragmode": "zoom",
                    "mapbox": {
                        "style": "light",
                        "center": {"lat": 37.1842803, "lon": -123.798209},
                        "zoom": 4,
                    },
                    "margin": {"r": 0, "t": 0, "b": 0, "l": 0, "pad": 0},
                    "showlegend": False,
                },
            },
            default=convert,
        )

class DistPlot(AbstractPlot):
    def __init__(
        self,
        name,
        x=None,
        y=None,
        x_label=None,
        y_label=None,
        key=None,
        bins=20,
    ) -> None:
        super().__init__(name, x=x, y=y, x_label=x_label, y_label=y_label, key=key)
        self.bins = bins

    def make_plot_img(self, data, ax):
        sn.histplot(data, x=self.x, bins=self.bins, ax=ax)

    def make_plot_json(self, data: pd.DataFrame):
        data2 = pd.cut(data[self.x], bins=self.bins).value_counts(sort=False)
        d = [go.Bar(x=list(data2.index.astype(str)), y=list(data2))]
        return json.dumps(d, cls=plotly.utils.PlotlyJSONEncoder)
