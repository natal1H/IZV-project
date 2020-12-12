#!/usr/bin/python3.8
# coding=utf-8

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
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
        reg_df = df[df["region"] == REGION]  # get only rows from our selected region

        # convert DataFrame to geopandas.GeoDataFrame
        gdf = geopandas.GeoDataFrame(reg_df, geometry=geopandas.points_from_xy(reg_df["d"], reg_df["e"]),
                                     crs="EPSG:5514")
        gdf = gdf[gdf["d"].notna()]  # drop rows where "d" is nan
        gdf = gdf[gdf["e"].notna()]  # drop rows where "e" is nan
        return gdf
    else:  # df is None
        raise ValueError("No DataFrame provided.")


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """
    Plot graph with two subplots based on accident location
    :param gdf: geopandas.GeoDataFrame containing accidents data
    :param fig_location: if not None, then location where to store figure
    :param show_figure: if True, will show the figure
    :return: doesn't return anything
    """
    fig, ax = plt.subplots(1, 2, squeeze=False, figsize=(12, 5), sharex=True, sharey=True)

    gdf[gdf["p5a"] == 1].plot(ax=ax[0, 0], markersize=1, color="r",  label="V obci")
    ctx.add_basemap(ax[0, 0], crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLite, alpha=0.9)
    ax[0, 0].set_title(f'Nehody v {REGION} kraji: v obci')
    ax[0, 0].set_axis_off()

    gdf[gdf["p5a"] == 2].plot(ax=ax[0, 1], markersize=1, color="g", label="Mimo obec")
    ctx.add_basemap(ax[0, 1], crs=gdf.crs.to_string(), source=ctx.providers.Stamen.TonerLite, alpha=0.9)
    ax[0, 1].set_title(f'Nehody v {REGION} kraji: mimo obce')
    ax[0, 1].set_axis_off()

    plt.tight_layout()

    if fig_location is not None:
        plt.savefig(fig_location)  # Store the figure

    if show_figure:
        plt.show()  # Show the figure


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None, show_figure: bool = False):
    """
    Plot graph with locations of all accidents in region clustered into cluster
    :param gdf: geopandas.GeoDataFrame containing accidents data
    :param fig_location: if not None, then location where to store figure
    :param show_figure: if True, will show the figure
    :return: doesn't return anything
    """

    gdf_c = gdf.to_crs("EPSG:5514")  # spravny system pro praci s velikostmi
    #gdf_c["area"] = gdf_c.area
    gdf_c = gdf_c.set_geometry(gdf_c.centroid).to_crs(epsg=3857)

    ax = gdf_c.plot(figsize=(15, 15), markersize=1, color="tab:gray")

    # creating the clusters
    # Prvním krokem je vytvoření matice X o rozměrech (2645, 2) obsahující souřadnice (x,y)
    coords = np.dstack([gdf_c.geometry.x, gdf_c.geometry.y]).reshape(-1, 2)

    # unsupervised learning
    db = sklearn.cluster.MiniBatchKMeans(n_clusters=15).fit(coords)

    # Vytvoříme gdf4 obsahující kopii gdf_c a přidaný sloupec cluster odpovídající labelu
    gdf4 = gdf_c.copy()
    gdf4["cluster"] = db.labels_

    # spojeni dohromad0 (funkce dissolve - geograficky ekvivalent groupby)
    # h agregujeme jako pocet (a přejmenujeme na cnt)
    gdf4 = gdf4.dissolve(by="cluster", aggfunc={"h": "count"}).rename(columns=dict(h="cnt"))

    gdf_coords = geopandas.GeoDataFrame(geometry=geopandas.points_from_xy(db.cluster_centers_[:, 0], db.cluster_centers_[:, 1]))

    gdf5 = gdf4.merge(gdf_coords, left_on="cluster", right_index=True).set_geometry("geometry_y")

    gdf5.plot(ax=ax, markersize=gdf5["cnt"], column="cnt", legend=True, alpha=0.6)
    ctx.add_basemap(ax, crs="epsg:3857", source=ctx.providers.Stamen.TonerLite, alpha=0.9)

    plt.axis("off")
    plt.title(f'Nehody v {REGION} kraji')

    if fig_location is not None:
        plt.savefig(fig_location)  # Store the figure

    if show_figure:
        plt.show()  # Show the figure


if __name__ == "__main__":
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    #plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

