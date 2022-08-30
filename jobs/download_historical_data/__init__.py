from ast import pattern
import os
import shutil
import wget
import zipfile38 as zipfile
from utils import get_working_day, get_n_trading_days, load_yaml
import re


#https://archives.nseindia.com/content/historical/DERIVATIVES/2022/JUL/fo11JUL2022bhav.csv.zip
#https://archives.nseindia.com/content/indices/ind_close_all_12072022.csv EQUITIES
class DownloadData:
    def __init__(self, **kwargs):
        params = kwargs.get('params')
        common = kwargs.get('common')
        self.segment = kwargs.get('segment')
        self.bhavcopy_dir = kwargs.get('bhavcopy_dir')
        if kwargs.get('download_url'):
            self.download_url = kwargs.get('download_url')
        else:
            self.download_url = params.nse_endpoint
        self.year = common.yyyy
        self.month_int = common.mm
        self.month = common.mm_str
        self.day = common.dd

        today = kwargs.get('date')
        if today:
            self.year = today.year
            self.month_int = today.strftime("%m")
            self.month = today.strftime("%b").upper()
            self.day = today.strftime("%d")


    def update_endpoint(self):
        if 'ind' in self.segment:
            pattern = re.compile(r'[\d]{8}.csv')
            self.download_url = re.sub(pattern, f'{self.day}{self.month_int}{self.year}.csv',self.download_url)
        elif 'eq' in self.segment.lower():
            pattern = re.compile(r'[\d]{4}/[\w]{3}/[\w]+')
            sub_str = f'{self.year}/{self.month}/cm{self.day}{self.month}{self.year}bhav'
            self.download_url = re.sub(pattern, sub_str,self.download_url)
        elif 'de' in self.segment.lower():
            pattern = re.compile(r'[\d]{4}/[\w]{3}/[\w]+')
            sub_str = f'{self.year}/{self.month}/fo{self.day}{self.month}{self.year}bhav'
            self.download_url = re.sub(pattern, sub_str,self.download_url)

    def prepare_urls(self):
        self.downloaded_bhavcopy = os.path.join(self.bhavcopy_dir,self.download_url.split('/')[-1])

    def download_data(self):
        print(f'From: {self.download_url} \n Into: {self.downloaded_bhavcopy}')
        wget.download(self.download_url, out=self.downloaded_bhavcopy)

    def unzip_file(self,zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_data:
            zip_infos = zip_data.infolist()
            for zip_info in zip_infos:
                zip_info.filename = f"{self.year}{self.month_int}{self.day}.csv"
                zip_data.extract(zip_info,path=self.bhavcopy_dir)

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
        self.download_data()
        print('-----------------------------Unziping-----------------------------')
        if 'ind' in self.segment:
            self.rename_file()
        else:
            self.unzip_file(self.downloaded_bhavcopy)
            print('-----------------------------Cleaning up-----------------------------')
            self.remove_unused_data(self.downloaded_bhavcopy)
        print('-----------------------------Data downloaded successfully-----------------------------')
