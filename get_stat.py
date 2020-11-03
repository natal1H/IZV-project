import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from download import DataDownloader


def plot_stat(data_source, fig_location=None, show_figure=False):
    if data_source is None:
        # TODO - raise error
        print("ERROR")

    # Create dictionary region name - number of accidents
    accidents = {"2016": None, "2017": None, "2018": None, "2019": None, "2020": None}  # TODO: nech si automaticky zisti ake roky tam su

    # Iterate over all accident records
    for i in range(data_source[1][0].size):
        # Check accident region
        region = data_source[1][data_source[0].index("region")][i]
        date = data_source[1][data_source[0].index("date")][i]
        year = date.split("-")[0]

        # Increase accident count
        if accidents[year] is None:
            accidents[year] = {region: 1}
        elif region not in accidents[year].keys():
            accidents[year][region] = 1
        else:
            accidents[year][region] += 1

    # find max number of accident to set y limit on graph (slightly bigger than it)
    accidents_by_years = [[num for region, num in stats.items()] for stats in accidents.values()]
    all_accidents = [inner for outer in accidents_by_years for inner in outer]  # join all nested lists into one list
    max_accidents = max(all_accidents)

    # prepare figure
    dpi = 96  # typical monitor dpi in order to get size in pixels we want
    plt.figure(figsize=(1000/dpi, 1600/dpi), dpi=dpi)
    plt.suptitle("Počty nehôd v krajoch Českej republiky")
    num_rows = len(accidents.keys())
    plot_index = 1

    for year, stats in accidents.items():
        plt.subplot(num_rows, 1, plot_index)
        regions = list(stats.keys())
        regions.sort()
        num_accidents = [stats[region] for region in regions]

        # get region order
        order = [
            sorted(num_accidents, reverse=True).index(num) + 1
            for num in num_accidents
        ]

        # making the graph
        plt.title(year)  # Subplot title
        plt.grid(axis="y", zorder=0)  # Horizontal grid
        plt.ylabel("Počet nehôd")  # Y label
        plt.ylim(top=max_accidents + 4000)
        plt.yticks(np.arange(0, max_accidents + 4000, 4000))
        plt.bar(regions, num_accidents, zorder=3)  # zorder has to be 3 so that grid is behind bars
        xlocs, xlabs = plt.xticks()
        plt.subplots_adjust(hspace=0.8)

        for i, v in enumerate(num_accidents):  # show exact number of accidents
            plt.text(xlocs[i] - 0.3, num_accidents[i] - 2000, num_accidents[i], fontsize=8)

        for i, v in enumerate(order):  # show region order in list of accidents sorted from max to min
            plt.text(xlocs[i] - 0.1, num_accidents[i] + 500, str(v))

        plot_index += 1

    # show or save figure
    if fig_location is not None:
        # check if folder where to save it exists
        folder = os.path.dirname(fig_location)
        if not os.path.exists(folder):
            os.makedirs(folder)
        plt.savefig(fig_location, dpi=dpi)
    if show_figure:  # figure location not set -> only show graph
        plt.show()

    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize graph of accidents.')
    parser.add_argument("--fig_location", type=str, help="figure location for saving")
    parser.add_argument("--show_figure", help="show figure", default=False, action="store_true")
    args = parser.parse_args()

    data = DataDownloader().get_list()
    plot_stat(data, fig_location=args.fig_location, show_figure=args.show_figure)
