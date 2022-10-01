
import os
from matplotlib.cbook import report_memory
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta
from utils import get_n_trading_days, create_dir,remove_files, get_working_day,check_if_file_exists
from jobs.generate_graph import GenerateDailyGraph
from jobs.generate_pdf import generate_pdf
from jobs.download_historical_data import DownloadData


class ProcessData:
    def __init__(self, **kwargs):
        self.today = get_working_day().strftime("%Y%m%d")
        self.params = kwargs.get('params')
        self.common = kwargs.get('common')
        self.symbols = kwargs.get('symbols')
        self.report_name = kwargs.get('report_name')
        self.bhavcopy_dir = kwargs.get('bhavcopy_dir')
        self.reports_dir = kwargs.get('reports_dir')
        self.reports_dir = os.path.join(self.reports_dir, self.common.business_date)
        self.graphs_dir = kwargs.get('graphs_dir')
        self.emas = kwargs.get('emas')

    def get_historical_ndays_df(self, dates):
        historical_ndays = []
        for dt in dates:
            d, m, y = dt.strftime("%d"),dt.strftime("%m"),dt.year
            bhavcopy = os.path.join(self.bhavcopy_dir, f"{y}{m}{d}.csv")
            if not check_if_file_exists(bhavcopy):
                download_bhavcopy = DownloadData(
                        params=self.params, 
                        common=self.common, 
                        segment=self.common.eq_segment, 
                        bhavcopy_dir=self.params.historical_data,
                        date=dt
                    )
                download_bhavcopy.update_endpoint()
                download_bhavcopy.start_downloading()
            bhavcopy_df = pd.read_csv(bhavcopy)
            historical_ndays.append(bhavcopy_df)
        return historical_ndays

    def make_data_plot_ready(self, historical_ndays_df):
        nifty = {}
        for symbol in self.symbols:
            stock = []
            for day in historical_ndays_df:
                day = day.loc[(day['SERIES'] == 'EQ') & (day['SYMBOL'] == symbol)]
                day = day[['OPEN', 'HIGH','LOW','CLOSE','TIMESTAMP','TOTTRDQTY']]
                stock.append(day)
            nifty[symbol] = stock
        return nifty

    def generate_graph(self,plot_ready_historical_data):
        graph = GenerateDailyGraph(self.graphs_dir)
        for key, value in plot_ready_historical_data.items():
            stock = pd.concat(value[::-1],ignore_index=True)
            stock.reset_index()
            stock.TIMESTAMP = pd.DatetimeIndex(stock['TIMESTAMP'])
            stock = stock.set_index('TIMESTAMP')
            stock.index.name = 'Date'
            stock = stock.rename(columns={'TOTTRDQTY': 'Volume'})
            stock = stock.rename(columns=lambda x: x.capitalize())
            graph.generate_graph(stock, key, show_volume=True, emas=self.emas)

    def make_required_dirs(self):
        create_dir(self.reports_dir)
        create_dir(self.graphs_dir)

    def clean_post_report(self):
        remove_files(self.graphs_dir, ext='png')

    def generate_pdf(self):
        generate_pdf(self.reports_dir, self.report_name, self.graphs_dir)

    def process_data(self):
        trading_days = max (self.params.trading_day, max(self.emas) + 10)
        dates = get_n_trading_days(trading_days)
        historical_ndays_df = self.get_historical_ndays_df(dates)
        plot_ready_historical_data = self.make_data_plot_ready(historical_ndays_df)
        self.make_required_dirs()
        self.generate_graph(plot_ready_historical_data)
        self.generate_pdf()
        self.clean_post_report()