import os
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta
from utils import *
from generate_daily_graph import GenerateDailyGraph


class ComputeDailyData:
    def __init__(self, historical_ndays=None):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.historical_data_dir = os.path.join(self.current_dir, "DailyHistoricalData")
        self.nifty_companies_dir = os.path.join(self.current_dir, "NiftyCompanies")
        self.report_dir = os.path.join(self.current_dir, "DailyReports")
        self.graph_save_dir = os.path.join(self.report_dir, "temp")
        self.historical_ndays = historical_ndays if historical_ndays else 20
        self.today = get_working_day().strftime("%Y%m%d")


    def compute_nifty_50(self):
        nifty_50_input_name =  os.path.join(self.nifty_companies_dir, "nifty_50.csv")
        nifty_50_df = pd.read_csv(nifty_50_input_name)
        nifty_50_df = nifty_50_df.loc[(nifty_50_df['Series'] == 'EQ')]
        report_name = f"Daily_Nifty_50_Report-{self.today}.pdf"
        self.start_computing(nifty_50_df["Symbol"].tolist(), report_name)

    def compute_next_nifty_50(self):
        nifty_100_input_name =  os.path.join(self.nifty_companies_dir, "nifty_100.csv")
        nifty_100_df = pd.read_csv(nifty_100_input_name)
        nifty_100_df = nifty_100_df.loc[(nifty_100_df['Series'] == 'EQ')]
        report_name = f"Daily_Next_Nifty_50_Report-{self.today}.pdf"
        self.start_computing(nifty_100_df["Symbol"].tolist(), report_name)

    def compute_mid_150(self):
        nifty_mid_150_input_name =  os.path.join(self.nifty_companies_dir, "nifty_mid_150.csv")
        nifty_mid_150_df = pd.read_csv(nifty_mid_150_input_name)
        nifty_mid_150_df = nifty_mid_150_df.loc[(nifty_mid_150_df['Series'] == 'EQ')]
        report_name = f"Daily_mid_150_Report-{self.today}.pdf"
        self.start_computing(nifty_mid_150_df["Symbol"].tolist(), report_name)

    def compute_small_250(self):
        nifty_small_250_input_name =  os.path.join(self.nifty_companies_dir, "nifty_small_250.csv")
        nifty_small_250_df = pd.read_csv(nifty_small_250_input_name)
        nifty_small_250_df = nifty_small_250_df.loc[(nifty_small_250_df['Series'] == 'EQ')]
        report_name = f"Daily_Small_250_Report-{self.today}.pdf"
        self.start_computing(nifty_small_250_df["Symbol"].tolist(), report_name)

    def compute_nifty_500(self):
        nifty_500_input_name =  os.path.join(self.nifty_companies_dir, "nifty_500.csv")
        nifty_500_df = pd.read_csv(nifty_500_input_name)
        nifty_500_df = nifty_500_df.loc[(nifty_500_df['Series'] == 'EQ')]
        report_name = f"Daily_Nifty_500_Report-{self.today}.pdf"
        self.start_computing(nifty_500_df["Symbol"].tolist(), report_name)

    def get_historical_ndays_df(self, dates):
        historical_ndays = []
        for dt in dates:
            d, m, y = dt.strftime("%d"),dt.strftime("%m"),dt.year
            historical_ndays.append(pd.read_csv(os.path.join(self.historical_data_dir, f"{y}{m}{d}.csv")))
        return historical_ndays

    def make_data_plot_ready_test(self, symbols, historical_ndays_df):
        nifty = {}
        for symbol in symbols:
            stock = []
            for day in historical_ndays_df:
                day = day.loc[(day['SERIES'] == 'EQ') & (day['SYMBOL'] == symbol)]
                daily_change = ((day["CLOSE"] - day["PREVCLOSE"])/day["CLOSE"]) * 100
                day["DAILY_RETURN"] = round(daily_change, 2)
                stock.append(day)
            nifty[symbol] = stock
        return nifty

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

    def generate_graph(self,plot_ready_historical_data):
        graph = GenerateDailyGraph()
        create_dir(self.graph_save_dir)
        for key, value in plot_ready_historical_data.items():
            stock = pd.concat(value[::-1],ignore_index=True)
            stock.reset_index()
            stock.TIMESTAMP = pd.DatetimeIndex(stock['TIMESTAMP'])
            stock = stock.set_index('TIMESTAMP')
            stock.index.name = 'Date'
            stock = stock.rename(columns={'TOTTRDQTY': 'Volume'})
            stock = stock.rename(columns=lambda x: x.capitalize())
            graph.generate_graph(stock, key, self.graph_save_dir )

    def start_computing(self):
        dates = get_n_trading_days(self.historical_ndays)
        historical_ndays_df = self.get_historical_ndays_df(dates)
        plot_ready_historical_data = self.make_data_plot_ready_test(["DMART"], historical_ndays_df)
        
        # self.generate_graph(plot_ready_historical_data)
        # report_dir = os.path.join(self.report_dir, self.today)
        # create_dir(report_dir)
        # generate_pdf(os.path.join(report_dir, report_name),self.graph_save_dir)
        # remove_files(self.graph_save_dir , 'png')
        for key, value in plot_ready_historical_data.items():
            stock = pd.concat(value[::-1],ignore_index=True)
            stock.reset_index()
            # total = round(stock["DAILY_RETURN"].sum(),2)
            # n = len(stock.index)
            #print(stock['CLOSE'])
            print(stock['CLOSE'])
            data = stock['CLOSE'].ewm(span=21, adjust=False).mean()
            v = stock['TOTTRDQTY'].rolling(window=20).mean()
            print(v)
            return 0
            #daily_rtn = stock["DAILY_RETURN"].tolist()
        return 0
        sd = stdev(daily_rtn)
        print(sd, sd * (252 ** (1/2)))
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.stats import norm
        import seaborn as sns
        # sns.displot(daily_rtn)
        # plt.show()
        sns.histplot(daily_rtn,kde=True)
        # x_axis = np.arange(-10, 10, 0.01)
        # plt.plot(x_axis, norm.pdf(x_axis, mean(daily_rtn), sd))
        plt.show()

ComputeDailyData(60).start_computing()


