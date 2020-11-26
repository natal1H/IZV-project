#!/usr/bin/env python3.8
# coding=utf-8
from distutils.command.register import register

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

B_IN_MB: int = 1048576  # 1 MB = 1 048 576 B


# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    if os.path.isfile(filename):  # data file exists
        df = pd.read_pickle(filename, compression="gzip")

        # create date column in DataFrame
        df["date"] = pd.to_datetime(df["p2a"], format="%Y-%m-%d", errors="coerce")

        # get memory usage before changing columns
        old_size = df.memory_usage(deep=True, index=True).sum() / B_IN_MB

        # change data types of certain columns
        to_int32_cols = ["p1", "p36", "p37", "weekday(p2a)", "p6", "r", "s"]  # columns that should be int32
        df[to_int32_cols] = df[to_int32_cols].replace(r'^\s*$', "-1", regex=True)  # fill missing values
        df[to_int32_cols] = df[to_int32_cols].astype("int32")
        df["p2a"] = df["date"]  # date column - just copy "date" column
        df["p2b"] = df["p2b"].apply(lambda x: (str(int(x) // 100) if (int(x) // 100 > 9)
                                               else "0" + str(int(x) // 100)) + ":" + (str(int(x) % 100)
                                               if (int(x) % 100 > 9) else "0" + str(int(x) % 100)))
        df["p2b"] = pd.to_datetime(df["p2b"], format="%H:%M", errors="coerce")
        to_string_cols = ["h", "i", "j", "l", "n", "o", "t", ]  # columns that should be string
        df[to_string_cols] = df[to_string_cols].astype("string")
        to_categories_cols = ["p", "q", "k"]
        df[to_categories_cols] = df[to_categories_cols].astype('category')

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

        sns.set()
        fig, axs = plt.subplots(4, 1, squeeze=False, figsize=(10, 10))

        ax = sns.barplot(ax=axs[0, 0], x="region", y="p13a", data=grouped_df,
                         order=grouped_df.sort_values('p1', ascending=False).region, palette='rocket')
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Úmrtia")

        ax = sns.barplot(ax=axs[1, 0], x="region", y="p13b", data=grouped_df,
                         order=grouped_df.sort_values('p1', ascending=False).region, palette='rocket')
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Ťažko ranení")

        ax = sns.barplot(ax=axs[2, 0], x="region", y="p13c", data=grouped_df,
                         order=grouped_df.sort_values('p1', ascending=False).region, palette='rocket')
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Ľahko ranení")

        ax = sns.barplot(ax=axs[3, 0], x="region", y="p1", data=grouped_df,
                         order=grouped_df.sort_values('p1', ascending=False).region, palette='rocket')
        ax.set(xlabel="", ylabel="Počet")
        ax.set_title("Celkom nehôd")

        plt.tight_layout()

        if fig_location is not None:
            plt.savefig(fig_location)

        if show_figure:
            plt.show()

    else:  # df is None
        print("Error! No DataFrame provided.", file=sys.stderr)


# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    if df is not None:
        regions = ['JHM', 'HKK', 'PLK', 'PHA']

        sns.set()
        fig, axs = plt.subplots(2, 2, squeeze=False, figsize=(15, 10))
        idx = 0  # subplot index

        for reg in regions:
            reg_df = df[df['region'] == reg]
            reg_df = reg_df[['region', 'p12', 'p53']]
            reg_df['damage_types_bins'] = pd.cut(x=reg_df['p12'], bins=[0, 200, 300, 400, 500, 600, 700],
                                                 labels=['nezaviněná řidičem', 'nepřiměřená rychlost jízdy',
                                                         'nesprávné předjíždění', 'nedání přednosti v jízdě',
                                                         'nesprávný způsob jízdy', 'technická závada vozidla'])
            reg_df['damage_bins'] = pd.cut(x=reg_df['p53'], bins=[0, 500, 2000, 5000, 10000, float("inf")],
                                           labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

            ax = sns.countplot(ax=axs[idx // 2, idx % 2], x="damage_bins", hue="damage_types_bins", data=reg_df)
            ax.set_title(reg)
            ax.set(xlabel="Škoda [tis. Kč]", ylabel="Počet")
            idx += 1

            # TODO - legend display
            #if idx < len(regions) - 1:
            #    plt.gca().legend().set_title('')
            #else:
            #    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)  # legend on the right
        plt.tight_layout()

        if fig_location is not None:
            plt.savefig(fig_location)

        if show_figure:
            plt.show()

    else:  # df is None
        print("Error! No DataFrame provided.", file=sys.stderr)


# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    if df is not None:
        regions = ['JHM', 'HKK', 'PLK', 'PHA']

        sns.set()
        fig, axs = plt.subplots(2, 2, squeeze=False, figsize=(14, 10))
        idx = 0  # subplot index

        tmp_df = df[['region', 'date', 'p1', 'p16']]
        table = pd.crosstab(index=[tmp_df.region, tmp_df.date], columns=[tmp_df.p16], colnames=['p16'])
        table = table.reset_index()
        table = table.rename(columns={1: "clean", 2: "dirty", 3: "wet", 4: "mud", 5: "salt",
                                      6: "no_salt", 7: "oil", 8: "snow", 9: "sudden_change", 0: "other"})

        for reg in regions:
            reg_df = table[table['region'] == reg]
            reg_df = reg_df.resample("M", on="date").sum()

            ax = reg_df.plot(ax=axs[idx // 2, idx % 2])
            ax.set_title(reg)
            ax.set(xlabel="Datum vzniku nehody", ylabel="Počet nehod")

            idx += 1

        plt.tight_layout()

        if fig_location is not None:
            plt.savefig(fig_location)

        if show_figure:
            plt.show()

    else:  # df is None
        print("Error! No DataFrame provided.", file=sys.stderr)


if __name__ == "__main__":
    # pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce
    df = get_dataframe("accidents.pkl.gz", verbose=False)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=False)
    plot_damage(df, "02_priciny.png", False)
    plot_surface(df, "03_stav.png", True)
