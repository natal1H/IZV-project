import matplotlib.pyplot as plt
from download import DataDownloader


def plot_stat(data_source, fig_location=None, show_figure=False):
    # TODO - check data_source if valid (not None)

    # Create dictionary region name - number of accidents
    accidents = {"2016": None, "2017": None, "2018": None, "2019": None, "2020": None} # TODO: nech si automaticky zisti ake roky tam su

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

    # TODO: find max number of accident to set y limit on graph (slightly bigger than it)

    # prepare figure
    plt.figure(figsize=(10, 10)) # TODO - nastaviť správne rozmery
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
        plt.bar(regions, num_accidents, zorder=3)  # zorder has to be 3 so that grid is behind bars
        xlocs, xlabs = plt.xticks()
        # plt.tight_layout(pad=2.0)
        plt.subplots_adjust(hspace=0.8)

        for i, v in enumerate(num_accidents):  # TODO - will display at bottom of bar, change it to below top
            #plt.text(i - .25, v / num_accidents[i] + 100, num_accidents[i])
            #plt.text(i - 0.3, num_accidents[i] - 2000, num_accidents[i], fontsize=8)
            plt.text(xlocs[i] - 0.3, num_accidents[i] - 2000, num_accidents[i], fontsize=8)

        for i, v in enumerate(order):
            plt.text(xlocs[i] - 0.1, num_accidents[i] + 500, str(v))

        plot_index += 1
    plt.show()
    plt.close()


data = DataDownloader().get_list()
#data_source = DataDownloader().get_list(["JHM", "PAK", "OLK"])
plot_stat(data)
