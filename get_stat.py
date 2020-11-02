import matplotlib
from download import DataDownloader

def plot_stat(data_source, fig_location = None, show_figure = False):
    # TODO - check data_source if valid (not None)

    # Create dictionary region name - number of accidents
    accidents = {"2016": None, "2017": None, "2018": None, "2019": None, "2020": None}

    # Iterate over all accident records
    for i in range(data_source[1][0].size):
        print(i, " ", end="")
        # Check accident region
        region = data_source[1][data_source[0].index("region")][i]
        date = data_source[1][data_source[0].index("date")][i]
        year = date.split("-")[0]
        print(region, date, year)

        # Increase accident count
        if accidents[year] is None:
            accidents[year] = {region: 1}
        elif region not in accidents[year].keys():
            accidents[year][region] = 1
        else:
            accidents[year][region] += 1

    print(accidents)

#data_source = DataDownloader().get_list(["JHM", "PAK", "OLK"])
dataDownloader = DataDownloader()
data_source = dataDownloader.get_list(["JHM", "PAK", "OLK"])
plot_stat(data_source)