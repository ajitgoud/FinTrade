
import os
from matplotlib.cbook import report_memory
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta
from utils import get_n_trading_days, create_dir,remove_files, get_working_day
from jobs.generate_graph import GenerateDailyGraph
from jobs.generate_pdf import generate_pdf


class ProcessData:
    def __init__(self, historical_ndays=None):
        self.today = get_working_day().strftime("%Y%m%d")

    def get_historical_ndays_df(self, dates, bhavcopy_dir):
        historical_ndays = []
        for dt in dates:
            d, m, y = dt.strftime("%d"),dt.strftime("%m"),dt.year
            historical_ndays.append(pd.read_csv(os.path.join(bhavcopy_dir, f"{y}{m}{d}.csv")))
        return historical_ndays

    def make_data_plot_ready(self, symbols, historical_ndays_df):
        nifty = {}
        for symbol in symbols:
            stock = []
            for day in historical_ndays_df:
                day = day.loc[(day['SERIES'] == 'EQ') & (day['SYMBOL'] == symbol)]
                day = day[['OPEN', 'HIGH','LOW','CLOSE','TIMESTAMP','TOTTRDQTY']]
                stock.append(day)
            nifty[symbol] = stock
        return nifty

    def generate_graph(self,plot_ready_historical_data,graphs_dir):
        emas = {
            'DAYS': [9,21],
            'WEEKS': [25,50],
            #'MONTHS': [50,100],
            #'LONGTERM': [100,200],
        }
        graph = GenerateDailyGraph(graphs_dir, emas)
        for key, value in plot_ready_historical_data.items():
            stock = pd.concat(value[::-1],ignore_index=True)
            stock.reset_index()
            stock.TIMESTAMP = pd.DatetimeIndex(stock['TIMESTAMP'])
            stock = stock.set_index('TIMESTAMP')
            stock.index.name = 'Date'
            stock = stock.rename(columns={'TOTTRDQTY': 'Volume'})
            stock = stock.rename(columns=lambda x: x.capitalize())
            graph.generate_graph(stock, key)

    def make_required_dirs(self, reports_dir, graph_save_dir):
        create_dir(reports_dir)
        create_dir(graph_save_dir)


    def clean_post_report(self,graph_save_dir):
        remove_files(graph_save_dir, ext='png')

    def generate_pdf(self, report_name, reports_dir, graph_save_dir):
        generate_pdf(reports_dir, report_name, graph_save_dir)

    def process_data(self, **kwargs):
        params = kwargs.get('params')
        common = kwargs.get('common')
        symbols = kwargs.get('symbols')
        report_name = kwargs.get('report_name')
        bhavcopy_dir = kwargs.get('bhavcopy_dir')
        reports_dir = kwargs.get('reports_dir')
        graphs_dir = kwargs.get('graphs_dir')

        dates = get_n_trading_days(params.trading_day)
        historical_ndays_df = self.get_historical_ndays_df(dates, bhavcopy_dir)
        plot_ready_historical_data = self.make_data_plot_ready(symbols, historical_ndays_df)
        reports_dir = os.path.join(reports_dir, common.business_date)
        self.make_required_dirs(reports_dir, graphs_dir)
        self.generate_graph(plot_ready_historical_data,graphs_dir)
        self.generate_pdf(report_name, reports_dir, graphs_dir)
        self.clean_post_report(graphs_dir)