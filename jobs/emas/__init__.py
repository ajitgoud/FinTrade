from email.message import EmailMessage
import os
import pandas as pd
from jobs.emas.process_data import ProcessData
from jobs.download_historical_data import DownloadData
from utils import *
import re


class Emas:
    def __init__(self, **kwargs):
        pass

    def download_bhavcopy(self, params, common):
        bhavcopy = os.path.join(params.historical_data, f'{common.business_date}.csv')
        if not check_if_file_exists(bhavcopy):
            download_bhavcopy = DownloadData(
                params=params, 
                common=common, 
                segment=common.eq_segment, 
                bhavcopy_dir=params.historical_data
                )
            download_bhavcopy.start_downloading()

    def initialize_task(self, task, params,common):
        input_file =  os.path.join(common.nifty_companies_dir, "nifty_500.csv")
        df = pd.read_csv(input_file)
        df = df.loc[(df['Series'] == 'EQ')]
        report_name = f"{task}_report-{common.business_date}.pdf"
        pattern = re.compile(r"[\d]+")
        emas = re.findall(pattern,task)
        emas = list(map(int, emas))
        ProcessData(
            params=params,
            common=common,
            symbols=df["Symbol"].tolist(), 
            report_name=report_name, 
            bhavcopy_dir = params.historical_data,
            reports_dir = params.reports,
            graphs_dir = common.graphs_dir,
            emas = emas
        ).process_data()

    def start(self, **kwargs):
        params = kwargs.get('params')
        common = kwargs.get('common')
        for task in params.tasks:
            if 'bhav' in task:
                self.download_bhavcopy(params.params,common)
            else:
                print(f'{task} task started')
                self.initialize_task(task, params.params,common)
                print(f'{task} task completed')

if __name__ == "__main__":
    eq = Emas()
    eq.download_bhavcopy()