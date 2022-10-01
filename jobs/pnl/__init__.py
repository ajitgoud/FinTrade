import os
import pandas as pd
from jobs.pnl.process_data import ProcessData
from utils import *
class Pnl:
    def __init__(self):
        self.cols = ['Symbol', 'Instrument', 'Entry date', 'Exit date', 'Weekday',
        'Entry price', 'Exit price', 'Long/Short', 'Position size', 'Stop loss',
        'Profit/Loss', 'Brokerage', 'Days held', 'Set up used',
        'Why this trade?', 'Learnings']
        self.today = get_working_day().strftime("%Y%m%d")

    def initialize_task(self, task, params,common):
        # tradebook = os.path.join(params.historical_data, f'Tradebook.xlsx')
        # res = len(tradebook.sheet_names)
        # print(res)
        report_name = f"PnL_report-{self.today}.pdf"
        ProcessData(
            params=params,
            common=common,
            report_name=report_name, 
            tradebook_dir = params.historical_data,
            reports_dir = params.reports,
            graphs_dir = common.graphs_dir
        ).process_data()

    def start(self, **kwargs):
        params = kwargs.get('params')
        common = kwargs.get('common')

        for task in params.tasks:
            print(f'{task} task started')
            self.initialize_task(task, params.params,common)
            print(f'{task} task completed')

if __name__ == '__main__':
    pnl = Pnl()
    pnl.read_pnl()