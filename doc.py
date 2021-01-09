#!/usr/bin/python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns
import numpy as np

"""IZV project - Final part
    Author: Natália Holková
    Login: xholko02
"""


def create_graph(df):
    # Get new DataFrame with only columns I need
    # df_new = df[["p1", "date", "p44", "p57"]]
    df_new = df[["p1", "date", "p44", "p57"]]
    # print(df_new.head())
    print("Before drop:", len(df_new))

    # only keep rows, where p44 (type of vehicle) is car or motorcycle (== 1/2/3/4)
    df_new = df_new[df_new["p44"].isin([1, 2, 3, 4])]
    df_new = df_new[df_new["p57"].isin([1, 6, 8])]

    print(df_new.head())
    print("After drop:", len(df_new))

    # grouped_df = df_new.groupby('p44')
    # grouped_df = grouped_df.reset_index()
    # print(grouped_df)

    table = df_new.pivot_table(index=["p44"], columns='p57', aggfunc='size', fill_value=0)
    print(table)

    # prepare for graph
    # df_for_graph = table

    """
    ##########
    sns.set()
    # fig, axs = plt.subplots(2, 2, squeeze=False, sharey="all", figsize=(15, 10))
    # plt.figure(figsize=(15, 10))

    # cut df by damage cause into bins, set labels
    df_new['vehicle_bins'] = pd.cut(x=df_new['p44'], bins=[0, 2, 4],
                                    labels=['motocykel', 'auto'])
    # cut df by damage size into bins, set labels
    # df_new['damage_bins'] = pd.cut(x=df_new['p53'], right=True,
    #                               bins=[-1, 499, 2000, 5000, 10000, float("inf")],
    #                               labels=['< 50', '50 - 200', '200 - 500', '500 - 1000', '> 1000'])

    # ax = sns.countplot(x="damage_bins", hue="damage_types_bins", data=df_new)
    # ax.set_title("TEST")
    # ax.set(xlabel="Škoda [tis. Kč]", ylabel="Počet")
    print("END")
    """

if __name__ == "__main__":
    #pass

    if os.path.isfile("accidents.pkl.gz"):  # data file exists
        df = pd.read_pickle("accidents.pkl.gz")
    else:  # data file does not exist
        raise FileNotFoundError("File accidents.pkl.gz containing data not found.")

    # create date column in DataFrame
    df["date"] = pd.to_datetime(df["p2a"], format="%Y-%m-%d", errors="coerce")
    create_graph(df)
