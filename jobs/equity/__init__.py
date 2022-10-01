import os
import pandas as pd
from jobs.equity.process_data import ProcessData
from jobs.download_historical_data import DownloadData
from utils import *


class Equity:
    def __init__(self, **kwargs):
        self.today = get_working_day().strftime("%Y%m%d")
        self.bhavcopy_dir = ''

    def download_bhavcopy(self, params, common):
        bhavcopy = os.path.join(params.historical_data, f'{self.today}.csv')
        if not check_if_file_exists(bhavcopy):
            download_bhavcopy = DownloadData(
                params=params, 
                common=common, 
                segment=common.eq_segment, 
                bhavcopy_dir=params.historical_data
                )
            download_bhavcopy.start_downloading()

    def initialize_task(self, task, params,common):
        input_file =  os.path.join(common.nifty_companies_dir, f"{task}.csv")
        df = pd.read_csv(input_file)
        df = df.loc[(df['Series'] == 'EQ')]
        report_name = f"{task}_report-{self.today}.pdf"
        ProcessData(
            params=params,
            common=common,
            symbols=df["Symbol"].tolist(), 
            report_name=report_name, 
            bhavcopy_dir = params.historical_data,
            reports_dir = params.reports,
            graphs_dir = common.graphs_dir
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
    eq = Equity()
    eq.download_bhavcopy()