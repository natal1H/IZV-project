#!/usr/bin/python3.8
# coding=utf-8

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily
import sklearn.cluster
import numpy as np

"""IZV project - Final part
    Author: Natália Holková
    Login: xholko02
"""

REGION = 'JHM'


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """
    Converts dataframe to geopandas.GeoDataFrame with correct encoding
    :param df: DataFrame containing accidents data
    :return: geopandas.GeoDataFrame
    """
    if df is not None:
        # convert DataFrame to geopandas.GeoDataFrame
        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514")
        gdf = gdf[gdf["d"].notna()]  # drop rows where "d" is nan
        gdf = gdf[gdf["e"].notna()]  # drop rows where "e" is nan
        return gdf
    else:  # df is None
        raise ValueError("No DataFrame provided.")


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

