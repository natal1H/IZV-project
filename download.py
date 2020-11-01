import requests, os, re, zipfile, csv, io, math
import numpy as np
from bs4 import BeautifulSoup
import timeit # for testing

class DataDownloader:
    csv_headers = [
        "p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9",
        "p10", "p11", "p12", "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", 
        "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28", "p34", "p35",
        "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53",
        "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "n", "o", "p", "q", "r", "s", "t", "p5a"
    ]

    region_filename = {
        "PHA": "00.csv", "STC": "01.csv", "JHC": "02.csv", "PLK": "03.csv", 
        "KVK": "19.csv", "ULK": "04.csv", "LBK": "18.csv", "HKK": "05.csv",
        "PAK": "17.csv", "OLK": "14.csv", "MSK": "07.csv", "JHM": "06.csv",
        "ZLK": "15.csv", "VYS": "16.csv"
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
            
            if table == None:
                # TODO - raise error
                print("ERROR")

            # Create output folder if doesn't exist
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            for link in table.find_all('a',class_='btn btn-sm btn-primary'):
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
            if year_file == None:
                # 2016 has format "datagis2016.zip" - check for that
                result = list(filter(lambda v: re.match(r"data[-]?gis[-]?{0}.zip".format(year), v), files))
                if len(result) != 0:
                    year_file = result[0]

            if year_file == None: # File with whole year stats is not present, need to find latest month file
                for month in range(12, 0, -1):
                    month_str = str(month) if month > 9 else "0" + str(month)
                    result = list(filter(lambda v: re.match(r"data[-]?gis[-]?{0}[-]?{1}.zip".format(month_str, year), v), files))
                    if len(result) != 0:
                        year_file = result[0]
                        break

            if year_file == None:
                # raise error? 
                print("ERROR")

            # read one csv file from zip archive
            print(self.folder + "/" + year_file, self.region_filename[region])
            with zipfile.ZipFile(self.folder + "/" + year_file) as zf:
                with zf.open(self.region_filename[region], 'r') as infile:
            #for tmp in range(1): # TODO - REMOVE!
            #    with open("test.csv", 'r') as infile:
                    reader = csv.reader(io.TextIOWrapper(infile, 'windows-1250'), delimiter=";")
                    #reader = csv.reader(infile, delimiter=";")
                    num_lines = 0
                    
                    #print(reader)
                    for lines in reader:
                        num_lines += 1
                        for i in range(len(self.csv_headers)):
                            # try to convert to int
                            #if re.match(r"^[-+]?\d+$", lines[i]):  # is integer
                            try:
                                if re.match(r"^[-+]?([1-9]\d*|0)$", lines[i]):  # is integer
                                    column_list[i].append(int(lines[i]))
                                #elif re.match(r"^[-+]?\d*\.\d+|\d+$", lines[i]):  # is float
                                elif re.match(r"^[-+]?\d*\.\d+|\d+$", lines[i]):  # is float
                                    column_list[i].append(float(lines[i]))
                                #elif re.match(r"^[-+]?\d*,\d+|\d+$", lines[i]):  # is float but needs to replace ","
                                elif re.match(r"^[-+]?\d*,\d+|\d+$", lines[i]):  # is float but needs to replace ","
                                    corrected_float = lines[i].replace(',', '.')
                                    column_list[i].append(float(corrected_float))
                                else: # is just normal string
                                    column_list[i].append(lines[i])
                            except ValueError: # TODO - poriesit lepsie '3.5kmsměrdálniceD1' -> chce davat na float
                                column_list[i].append(lines[i])

                    column_list[-1] = column_list[-1] + (num_lines * [region])
            #break # TODO - testing only for one year

        # TODO - clean the values! - "" kedy ma byt str a kedy NaN, ...

        for i in range(len(np_list)):
            np_list[i] = np.asarray(column_list[i])
        #print(np_list)
        return (self.csv_headers + ["region"], np_list)
            

    def get_list(self, regions = None):
        pass


# Main
dataDownloader = DataDownloader()
#dataDownloader.download_data()
ret = dataDownloader.parse_region_data("PHA")
print(ret)
print("END")