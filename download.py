import requests, os
from bs4 import BeautifulSoup

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

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/",folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder # TODO: check if "/" is at the end - remove if it is
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
                    print("Downloading: {}".format(link["href"]))
                    with open(save_path, 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=128):
                            fd.write(chunk)
            print("Download done.")

        else:
            # TODO - raise error 
            print("ERROR")

    def parse_region_data(self, region):
        # TODO - if data are not downloaded - download them (check if folder empty??)
        
        if region not in self.region_filename.keys():
            # TODO - raise error
            print("ERROR")


    def get_list(self, regions = None):
        pass


# Main
dataDownloader = DataDownloader()
dataDownloader.download_data()