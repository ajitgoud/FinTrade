import os
import shutil
import wget
import zipfile38 as zipfile
from utils import get_working_day, get_n_trading_days


#https://archives.nseindia.com/content/historical/DERIVATIVES/2022/JUL/fo11JUL2022bhav.csv.zip
#https://archives.nseindia.com/content/indices/ind_close_all_12072022.csv EQUITIES
class DownloadData:
    def __init__(self, **kwargs):
        base_historical_url="https://archives.nseindia.com/content/"
        self.segment = kwargs.get('segment')
        if not 'ind' in self.segment:
            base_historical_url=f"{base_historical_url}/historical"
        self.segment_url=f"{base_historical_url}/{self.segment}"
        self.bhavcopy_dir = kwargs.get('bhavcopy_dir')
        if kwargs.get('date'):
            today = kwargs.get('date')
        else:
            today = get_working_day()
        self.day, self.month_int, self.year, self.month = today.strftime("%d"), today.strftime("%m"),today.year, today.strftime("%b").upper()
                                      
    def prepare_urls(self):
        segment = self.segment.lower()
        if segment == 'indices': 
            bhavcopy = f"ind_close_all_{self.day}{self.month_int}{self.year}.csv" 
            self.bhavcopy_url = f"{self.segment_url}/{bhavcopy}"
        else:
            if 'eq' in segment:
                bhavcopy = f"cm{self.day}{self.month}{self.year}bhav.csv.zip"
            elif 'der' in segment:
                bhavcopy = f"fo{self.day}{self.month}{self.year}bhav.csv.zip"
            self.bhavcopy_url = f"{self.segment_url}/{self.year}/{self.month}/{bhavcopy}"
        self.downloaded_bhavcopy = os.path.join(self.bhavcopy_dir,bhavcopy)

    def download_data(self, url):
        print(url)
        wget.download(url, out=self.downloaded_bhavcopy)

    def unzip_file(self,zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_data:
            zip_infos = zip_data.infolist()
            for zip_info in zip_infos:
                zip_info.filename = f"{self.year}{self.month_int}{self.day}.csv"
                zip_data.extract(zip_info,path=self.bhavcopy_dir)

    def move_data(self):
        filename = f"{self.year}{self.month_int}{self.day}.csv"
        csv_bhavcopy_src = os.path.join(self.segment_url,filename)
        csv_bhavcopy_dest = os.path.join(self.csv_bhavcopy, filename)
        shutil.move(csv_bhavcopy_src, csv_bhavcopy_dest)

    def remove_unused_data(self, file):
        os.remove(file)

    def rename_file(self):
        self.downloaded_bhavcopy, f"{self.year}{self.month_int}{self.day}.csv"
        shutil.move(self.downloaded_bhavcopy, os.path.join(self.bhavcopy_dir,f"{self.year}{self.month_int}{self.day}.csv"))
    
    def start_downloading(self):
        print('-----------------------------Starting downloaded-----------------------------')
        print('-----------------------------Preparing URLS-----------------------------')
        self.prepare_urls()
        print('-----------------------------Downloading data-----------------------------')
        self.download_data(self.bhavcopy_url)
        print('-----------------------------Unziping-----------------------------')
        if 'ind' in self.segment:
            self.rename_file()
        else:
            self.unzip_file(self.downloaded_bhavcopy)
            print('-----------------------------Cleaning up-----------------------------')
            self.remove_unused_data(self.downloaded_bhavcopy)
        print('-----------------------------Data downloaded successfully-----------------------------')


if __name__ == '__main__':


    data_to_download = get_n_trading_days(1)

    for d in data_to_download:
        download = DownloadData(date=d)
        download.start_downloading()