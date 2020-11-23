#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import sys
import gzip
# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

"""IZV project - 2nd part
    Author: Natália Holková
    Login: xholko02
"""

B_IN_MB = 1048576 # 1 MB = 1 048 576 B

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    if os.path.isfile(filename):  # data file exists
        df = pd.read_pickle(filename, compression="gzip")

        # create date column in DataFrame
        df["date"] = pd.to_datetime(df["p2a"], format="%Y-%m-%d", errors="coerce")

        # get memory usage before changing columns
        old_size = df.memory_usage(deep=True, index=True).sum() / B_IN_MB

        # change data types of certain columns
        toInt32Cols = ["p1", "p36", "p37", "weekday(p2a)", "p6", "r", "s"]  # columns that should be int32
        df[toInt32Cols] = df[toInt32Cols].replace(r'^\s*$', "-1", regex=True)  # fill missing values
        df[toInt32Cols] = df[toInt32Cols].astype("int32")
        df["p2a"] = df["date"] # date column - just copy "date" column
        df["p2b"] = df["p2b"].apply(lambda x: (str(int(x) // 100) if (int(x) // 100 > 9) \
                                              else "0" + str(int(x) // 100) ) + ":" + (str(int(x) % 100) \
                                              if (int(x) % 100 > 9) else "0" + str(int(x) % 100)) )
        df["p2b"] = pd.to_datetime(df["p2b"], format="%H:%M", errors="coerce")
        toStringCols = ["h", "i", "j", "l", "n", "o", "t", ]  # columns that should be string
        df[toStringCols] = df[toStringCols].astype("string")
        toCategoriesCols = ["p", "q", "k"]
        df[toCategoriesCols] = df[toCategoriesCols].astype('category')

        # get new size
        new_size = df.memory_usage(deep=True, index=True).sum() / B_IN_MB

        if verbose:
            print("old_size={} MB".format(round(old_size, 1)))
            print("new_size={} MB".format(round(new_size, 1)))

        return df

    else:  # data file does not exist
        print("Error! File {} does not exist.".format(filename), file=sys.stderr)
        return None


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    if df is not None: 
        grouped_df = df.groupby('region').agg({'p1': 'count', 'p13a': 'sum', 'p13b': 'sum', 'p13c': 'sum'})
        grouped_df = grouped_df.reset_index()
        #print(grouped_df.head())

        sns.set()
        fig, axs = plt.subplots(4, 1, squeeze=False, figsize=(10, 10))

        ax = sns.barplot(ax=axs[0, 0], x="region", y="p13a", data=grouped_df, order=grouped_df.sort_values('p1', ascending=False).region)
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Úmrtia")

        ax = sns.barplot(ax=axs[1, 0], x="region", y="p13b", data=grouped_df, order=grouped_df.sort_values('p1', ascending=False).region)
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Ťažko ranení")

        ax = sns.barplot(ax=axs[2, 0], x="region", y="p13c", data=grouped_df, order=grouped_df.sort_values('p1', ascending=False).region)
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Ľahko ranení")

        ax = sns.barplot(ax=axs[3, 0], x="region", y="p1", data=grouped_df, order=grouped_df.sort_values('p1', ascending=False).region)
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Celkom nehôd")

        plt.tight_layout()

        if fig_location is not None:
            plt.savefig(fig_location)

        if show_figure:
            plt.show()


    else: # df is None
        print("Error! No DataFrame provided.", file=sys.stderr)

# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    pass

# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    pass


if __name__ == "__main__":
    #pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce
    df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    #plot_damage(df, "02_priciny.png", True)
    #plot_surface(df, "03_stav.png", True)
