#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import sys
import gzip
import resource  # TODO - je povolene?
import pickle
#import pickle5 as pickle
# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

"""IZV project - 2nd part
    Author: Natália Holková
    Login: xholko02
"""

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    if os.path.isfile(filename):  # data file exists
        print(filename)
        print(resource.getrlimit(resource.RLIMIT_STACK))
        print(sys.getrecursionlimit())

        max_rec = 0x100000

        # May segfault without this line. 0x100 is a guess at the size of each stack frame.
        resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
        sys.setrecursionlimit(max_rec)
        #sys.setrecursionlimit(1000000)
        print(sys.getrecursionlimit())


        #with gzip.open(filename, 'rb') as f:
            #df = pickle.load(f)
        #    df = pd.read_pickle(filename)
        #    print("Data loaded.")
            #print(df.p1)
            #print(df)
        #df = pd.read_pickle(filename, compression="gzip")
        df = pd.read_pickle("accidents.pkl")
        print("Data loaded.")
        print(df.p2a)

        return None

    else:  # data file does not exist
        print("Error! File {} does not exist.".format(filename), file=sys.stderr)
        return None


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    pass

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
    # funkce.
    print("Run main")
    df = get_dataframe("accidents.pkl.gz")
    #plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    #plot_damage(df, "02_priciny.png", True)
    #plot_surface(df, "03_stav.png", True)
    print("Main end")
