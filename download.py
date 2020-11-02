import requests, os, re, zipfile, csv, io, pickle
import numpy as np
from bs4 import BeautifulSoup


class DataDownloader:
    #csv_headers = [
    #    "p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9",
    #    "p10", "p11", "p12", "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17",
    #    "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28", "p34", "p35",
    #    "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53",
    #    "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    #    "n", "o", "p", "q", "r", "s", "t", "p5a"
    #]
    csv_headers = [
        "id", "p36", "p37", "date", "weekday", "time", "type", "type_driving_vehicles",
        "type_fixed_obstacle", "accident_character", "accident_fault", "alcohol_in_culprit", "main_cause",
        "dead", "seriously_injured", "lightly_injured", "total_material_damage", "road_surface", "road_during_accident",
        "road_state", "weather_conditions", "visibility", "visual_conditions", "road_division", "accident_placement",
        "traffic management", "local_driving_change", "specific_places_objects", "directional_conditions",
        "number_vehicles", "traffic_accident_location", "crossing_type", "vehicle_type", "vehicle_manufacturer",
        "vehicle_year", "vehicle_characteristic", "skid", "vehicle_after", "leakage", "rescue_from_vehicle",
        "driving_direction", "vehicle_damage", "driver_category", "drive_state", "driver_external_influence", "a", "b",
        "x_coord", "y_coord", "f", "g", "h", "i", "j", "k", "l",
        "n", "o", "p", "q", "r", "s", "t", "accident_location"
    ]

    region_filename = {
        "PHA": "00.csv", "STC": "01.csv", "JHC": "02.csv", "PLK": "03.csv", 
        "KVK": "19.csv", "ULK": "04.csv", "LBK": "18.csv", "HKK": "05.csv",
        "PAK": "17.csv", "OLK": "14.csv", "MSK": "07.csv", "JHM": "06.csv",
        "ZLK": "15.csv", "VYS": "16.csv"
    }

    region_cache = {
        "PHA": None, "STC": None, "JHC": None, "PLK": None,
        "KVK": None, "ULK": None, "LBK": None, "HKK": None,
        "PAK": None, "OLK": None, "MSK": None, "JHM": None,
        "ZLK": None, "VYS": None
    }

    years = ['2016', '2017', '2018', '2019', '2020']

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/",folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder  # TODO: check if "/" is at the end - remove if it is
        self.cache_filename = cache_filename

    def download_data(self):
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }

        resp = requests.get(self.url, headers = headers)
        if resp.status_code == 200:
            soup=BeautifulSoup(resp.text, 'html.parser')
            table = soup.find('table',class_='table table-fluid')
            
            if table is None:
                # TODO - raise error
                print("ERROR")

            # Create output folder if doesn't exist
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            for link in table.find_all('a', class_='btn btn-sm btn-primary'):
                download_path = self.url + link["href"]
                save_path = self.folder + "/" + os.path.basename(link["href"])
                
                with requests.get(download_path, stream=True) as r:
                    with open(save_path, 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=128):
                            fd.write(chunk)

        else:
            # TODO - raise error 
            print("ERROR")

    def parse_region_data(self, region):
        # TODO - if data are not downloaded - download them (check if folder empty??)
        
        if region not in self.region_filename.keys():
            # TODO - raise error
            print("ERROR")

        # Get list of files in folder
        all_files = [
            f 
            for f in os.listdir(self.folder) 
            if os.path.isfile(os.path.join(self.folder, f))
        ]

        # prepare the tuple
        np_list = (len(self.csv_headers) + 1) * [np.array([])]
        column_list = (len(self.csv_headers) + 1) * [None]
        for i in range(len(column_list)):
            column_list[i] = []

        for year in self.years:
            # get all files with 'year' in name
            files = [s for s in all_files if year in s]

            # find if exists file with statistics for whole year
            year_file = next((s for s in files if "rok" in s), None)
            if year_file is None:
                # 2016 has format "datagis2016.zip" - check for that
                result = list(filter(lambda v: re.match(r"data[-]?gis[-]?{0}".format(year), v), files))
                if len(result) != 0:
                    year_file = result[0]

            if year_file is None: # File with whole year stats is not present, need to find latest month file
                for month in range(12, 0, -1):
                    month_str = str(month) if month > 9 else "0" + str(month)
                    result = list(filter(lambda v: re.match(r"data[-]?gis[-]?{0}[-]?{1}".format(month_str, year), v), files))
                    if len(result) != 0:
                        year_file = result[0]
                        break

            if year_file is None:
                # raise error? 
                print("ERROR")

            # read one csv file from zip archive
            print(self.folder + "/" + year_file, self.region_filename[region])
            with zipfile.ZipFile(self.folder + "/" + year_file) as zf:
                with zf.open(self.region_filename[region], 'r') as infile:
                    reader = csv.reader(io.TextIOWrapper(infile, 'windows-1250'), delimiter=";")
                    num_lines = 0
                    
                    for lines in reader:
                        num_lines += 1
                        for i in range(len(self.csv_headers)):
                            # try to convert to int
                            try:
                                # if re.match(r"^[-+]?\d+$", lines[i]):  # is integer
                                if re.match(r"^[-+]?([1-9]\d*|0)$", lines[i]):  # is integer
                                    column_list[i].append(int(lines[i]))
                                elif re.match(r"^[-+]?\d*\.\d+|\d+$", lines[i]):  # is float
                                    column_list[i].append(float(lines[i]))
                                elif re.match(r"^[-+]?\d*,\d+|\d+$", lines[i]):  # is float but needs to replace ","
                                    corrected_float = lines[i].replace(',', '.')
                                    column_list[i].append(float(corrected_float))
                                elif len(lines[i]) == 0:  # empty string
                                    column_list[i].append(None)
                                else:  # is just normal string
                                    column_list[i].append(lines[i])
                            except ValueError:  # TODO - poriesit lepsie '3.5kmsměrdálniceD1' -> chce davat na float
                                column_list[i].append(lines[i])

                    column_list[-1] = column_list[-1] + (num_lines * [region])
            #break # TODO - testing only for one year

        # TODO - clean the values! - "" kedy ma byt str a kedy NaN, ...

        for i in range(len(np_list)):
            np_list[i] = np.asarray(column_list[i])
        #print(np_list)
        return (self.csv_headers + ["region"], np_list)
            

    def get_list(self, regions = None):
        if regions is None:
            regions = self.region_filename.keys()
        else:  # Check if all region names are correct
            for region in regions:
                if region not in self.region_filename.keys():
                    # TODO - raise error
                    print("ERROR")
                    break

        # prepare the tuple
        np_list = (len(self.csv_headers) + 1) * [np.array([])]
        for region in regions:
            print(region)
            # check if region data already loaded in class attribute
            if self.region_cache[region] is not None:
                data = self.region_cache[region]
            else:  # check if region data already stored as cache file
                region_cache_filename = self.cache_filename.replace("{}", region)
                if os.path.isfile(region_cache_filename): # cache file exists
                    with open(region_cache_filename, 'rb') as f:
                        data = pickle.load(f)
                        self.region_cache[region] = data
                else:  # region data not yet cached
                    data = self.parse_region_data(region)
                    self.region_cache[region] = data  # cache data in attribute
                    with open(region_cache_filename, 'wb') as f:  # Create cache file
                         pickle.dump(data, f)

            # Append acquired data to np array
            for i in range(len(np_list)):
                if np_list[i].size == 0:
                    np_list[i] = data[1][i]
                else:
                    np_list[i] = np.concatenate((np_list[i], data[1][i]))
            #print(region, "done.")

        return (self.csv_headers + ["region"], np_list)
        

if __name__ == "__main__":
    dataDownloader = DataDownloader()
    data = dataDownloader.get_list(["JHM", "PAK", "OLK"])
    #data = dataDownloader.get_list()
    # TODO - vypisat zakladne informacie o datach