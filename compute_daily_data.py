from enum import Flag
import os
from matplotlib.cbook import report_memory
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta
from utils import get_n_trading_days, generate_pdf, create_dir,remove_files, get_working_day
from generate_daily_graph import GenerateDailyGraph
from constant import *


class ComputeDailyData:
    def __init__(self, historical_ndays=None):
        self.today = get_working_day().strftime("%Y%m%d")
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.historical_data_dir = os.path.join(self.current_dir, HISTORICAL_DATA_DIRNAME)
        self.nifty_companies_dir = os.path.join(self.current_dir, "NiftyCompanies")
        self.report_dir = os.path.join(self.current_dir, "DailyReports")
        self.graph_save_dir = os.path.join(self.report_dir, "temp")
        self.report_dir = os.path.join(self.report_dir,self.today)
        self.historical_ndays = historical_ndays if historical_ndays else 20
        self.temp_subs = ['daily','ema_9_21','ema_25_50','ema_50_100','ema_100_200']


    def compute_nifty_50(self):
        nifty_50_input_name =  os.path.join(self.nifty_companies_dir, "nifty_50.csv")
        nifty_50_df = pd.read_csv(nifty_50_input_name)
        nifty_50_df = nifty_50_df.loc[(nifty_50_df['Series'] == 'EQ')]
        report_name = f"Nifty_50_Report-{self.today}.pdf"
        self.start_computing(nifty_50_df["Symbol"].tolist(), report_name)

    def compute_next_nifty_50(self):
        nifty_100_input_name =  os.path.join(self.nifty_companies_dir, "nifty_100.csv")
        nifty_100_df = pd.read_csv(nifty_100_input_name)
        nifty_100_df = nifty_100_df.loc[(nifty_100_df['Series'] == 'EQ')]
        report_name = f"Next_Nifty_50_Report-{self.today}.pdf"
        self.start_computing(nifty_100_df["Symbol"].tolist(), report_name)

    def compute_mid_150(self):
        nifty_mid_150_input_name =  os.path.join(self.nifty_companies_dir, "nifty_mid_150.csv")
        nifty_mid_150_df = pd.read_csv(nifty_mid_150_input_name)
        nifty_mid_150_df = nifty_mid_150_df.loc[(nifty_mid_150_df['Series'] == 'EQ')]
        report_name = f"Mid_150_Report-{self.today}.pdf"
        self.start_computing(nifty_mid_150_df["Symbol"].tolist(), report_name)

    def compute_small_250(self):
        nifty_small_250_input_name =  os.path.join(self.nifty_companies_dir, "nifty_small_250.csv")
        nifty_small_250_df = pd.read_csv(nifty_small_250_input_name)
        nifty_small_250_df = nifty_small_250_df.loc[(nifty_small_250_df['Series'] == 'EQ')]
        report_name = f"Small_250_Report-{self.today}.pdf"
        self.start_computing(nifty_small_250_df["Symbol"].tolist(), report_name)

    def compute_nifty_500(self):
        nifty_500_input_name =  os.path.join(self.nifty_companies_dir, "nifty_500.csv")
        nifty_500_df = pd.read_csv(nifty_500_input_name)
        nifty_500_df = nifty_500_df.loc[(nifty_500_df['Series'] == 'EQ')]
        report_name = f"Nifty_500_Report-{self.today}.pdf"
        self.start_computing(nifty_500_df["Symbol"].tolist(), report_name)

    def get_historical_ndays_df(self, dates):
        historical_ndays = []
        for dt in dates:
            d, m, y = dt.strftime("%d"),dt.strftime("%m"),dt.year
            historical_ndays.append(pd.read_csv(os.path.join(self.historical_data_dir, f"{y}{m}{d}.csv")))
        return historical_ndays

    def make_data_plot_ready(self, symbols, historical_ndays_df):
        nifty = {}
        for symbol in symbols:
            stock = []
            flag = False
            for day in historical_ndays_df:
                day = day.loc[(day['SERIES'] == 'EQ') & (day['SYMBOL'] == symbol)]
                if not flag:
                    flag=True
                    print(f'SYm: {symbol} {day}')
                day = day[['OPEN', 'HIGH','LOW','CLOSE','TIMESTAMP','TOTTRDQTY']]
                stock.append(day)
            nifty[symbol] = stock
        return nifty

    def generate_graph(self,plot_ready_historical_data):
        emas = {
            'DAYS': [9,21],
            'WEEKS': [25,50],
            #'MONTHS': [50,100],
            #'LONGTERM': [100,200],
        }
        graph = GenerateDailyGraph(self.graph_save_dir, emas)
        for key, value in plot_ready_historical_data.items():
            stock = pd.concat(value[::-1],ignore_index=True)
            # ls = value[0]
            # print(f'Symbol: {key} Close: {ls.CLOSE}')
            stock.reset_index()
            stock.TIMESTAMP = pd.DatetimeIndex(stock['TIMESTAMP'])
            stock = stock.set_index('TIMESTAMP')
            stock.index.name = 'Date'
            stock = stock.rename(columns={'TOTTRDQTY': 'Volume'})
            stock = stock.rename(columns=lambda x: x.capitalize())
            graph.generate_graph(stock, key)

    def make_required_dirs(self):
        create_dir(self.report_dir)
        create_dir(self.graph_save_dir, self.temp_subs)


    def clean_post_report(self,):
        remove_files(self.graph_save_dir , self.temp_subs, 'png')

    def generate_pdf(self, report_name):
        generate_pdf(self.report_dir, report_name, self.graph_save_dir, self.temp_subs)

    def start_computing(self, symbols, report_name):
        dates = get_n_trading_days(self.historical_ndays)
        historical_ndays_df = self.get_historical_ndays_df(dates)
        plot_ready_historical_data = self.make_data_plot_ready(symbols, historical_ndays_df) #symbols["DMART", "NTPC", "HDFC", "EICHERMOT"]
        self.make_required_dirs()
        self.generate_graph(plot_ready_historical_data)
        self.generate_pdf(report_name)
        self.clean_post_report()