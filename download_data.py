import os
import shutil
import wget
import zipfile38 as zipfile
from utils import get_working_day



class DownloadData:
    def __init__(self, day=None, month_int=None, year=None, month=None):
        self.base_historical_url="https://archives.nseindia.com/content/historical"
        self.equities_url=f"{self.base_historical_url}/EQUITIES"
        self.bhavcopy_base_path = os.path.dirname(os.path.realpath(__file__))
        if (day and month) and (year and month_int):
            self.day, self.month_int, self.year, self.month = day, month_int, year, month
        else:
            today = get_working_day()
            self.day, self.month_int, self.year, self.month = today.strftime("%d"), today.strftime("%m"),today.year, today.strftime("%b").upper()
                                      
    def prepare_urls(self):
        bhav_filename = f"cm{self.day}{self.month}{self.year}bhav.csv.zip"
        self.todays_bhavcopy_url = f"{self.equities_url}/{self.year}/{self.month}/{bhav_filename}"
        self.zip_bhavcopy = os.path.join(self.bhavcopy_base_path,bhav_filename)
        self.csv_bhavcopy = os.path.join(self.bhavcopy_base_path,"DailyHistoricalData")

    def download_data(self, url):
        print(url)
        #https://archives.nseindia.com/content/historical/EQUITIES/2022/JUN/cm30JUN2022bhav.csv.zip
        wget.download(url)

    def unzip_file(self,zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_data:
            zip_infos = zip_data.infolist()
            for zip_info in zip_infos:
                zip_info.filename = f"{self.year}{self.month_int}{self.day}.csv"
                zip_data.extract(zip_info)

    def move_data(self):
        filename = f"{self.year}{self.month_int}{self.day}.csv"
        csv_bhavcopy_src = os.path.join(self.bhavcopy_base_path,filename)
        csv_bhavcopy_dest = os.path.join(self.csv_bhavcopy, filename)
        shutil.move(csv_bhavcopy_src, csv_bhavcopy_dest)

    def remove_unused_data(self, file):
        os.remove(file)
    
    def start_downloading(self):
        print('-----------------------------Starting downloaded-----------------------------')
        print('-----------------------------Preparing URLS-----------------------------')
        self.prepare_urls()
        print('-----------------------------Downloading data-----------------------------')
        self.download_data(self.todays_bhavcopy_url)
        print('-----------------------------Unziping-----------------------------')
        self.unzip_file(self.zip_bhavcopy)
        print('-----------------------------Moving csv-----------------------------')
        self.move_data()
        print('-----------------------------Cleaning up-----------------------------')
        self.remove_unused_data(self.zip_bhavcopy)
        print('-----------------------------Data downloaded successfully-----------------------------')


if __name__ == '__main__':


    data_to_download = [
        ['31', '05', '2022', 'MAY'],
        ['30', '05', '2022', 'MAY'],
        ['27', '05', '2022', 'MAY'],
        ['26', '05', '2022', 'MAY'],
        ['25', '05', '2022', 'MAY'],
        ['24', '05', '2022', 'MAY'],
        ['23', '05', '2022', 'MAY'],
        ['20', '05', '2022', 'MAY'],
        ['19', '05', '2022', 'MAY'],
        ['18', '05', '2022', 'MAY'],
        ['17', '05', '2022', 'MAY'],
        ['16', '05', '2022', 'MAY']

    ]

    for d in data_to_download:
        download = DownloadData(*d)
        download.start_downloading()