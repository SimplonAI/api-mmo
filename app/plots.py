from abc import ABCMeta, abstractmethod
from slugify import slugify

import matplotlib.pyplot as plt
import seaborn as sn

class AbstractPlot(metaclass=ABCMeta):
    def __init__(self, name, x=None, y=None, x_label=None, y_label=None, key=None) -> None:
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
    def plot(self, data):
        pass

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
    def plot(self, data):
        fig, ax = plt.subplots(1)
        sn.scatterplot(self.x, self.y, data=data, ax=ax)
        
        ax.set_title(self.name)
        if self.x_label is not None:
            ax.set_xlabel(self.x_label)
        if self.y_label is not None:
            ax.set_ylabel(self.y_label)
        fig.tight_layout()

        return fig
