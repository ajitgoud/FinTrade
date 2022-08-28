
import os
from matplotlib.cbook import report_memory
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta
from utils import get_n_trading_weeks, create_dir,remove_files, get_working_day, check_if_file_exists
from jobs.generate_graph import GenerateDailyGraph
from jobs.generate_pdf import generate_pdf
from jobs.download_historical_data import DownloadData


class ProcessData:
    def __init__(self, **kwargs):
        self.params = kwargs.get('params')
        self.common = kwargs.get('common')
        self.indices = kwargs.get('indices')
        self.report_name = kwargs.get('report_name')
        self.bhavcopy_dir = kwargs.get('bhavcopy_dir')
        self.reports_dir = kwargs.get('reports_dir')
        self.reports_dir = os.path.join(self.reports_dir, self.common.business_date)
        self.graphs_dir = kwargs.get('graphs_dir')

    def get_historical_ndays_df(self, dates):
        historical_ndays_ls = []
        for dts in dates:
            historical_ndays = []
            for dt in dts:
                d, m, y = dt.strftime("%d"),dt.strftime("%m"),dt.year
                bhavcopy = os.path.join(self.bhavcopy_dir, f"{y}{m}{d}.csv")
                if not check_if_file_exists(bhavcopy):
                    download_bhavcopy = DownloadData(
                            params=self.params, 
                            common=self.common, 
                            segment=self.common.indices_segment, 
                            bhavcopy_dir=self.params.historical_data,
                            date=dt
                        )
                    download_bhavcopy.update_endpoint()
                    download_bhavcopy.start_downloading()

                bhavcopy_df = pd.read_csv(bhavcopy)
                bhavcopy_df["Index Date"] = bhavcopy_df["Index Date"].apply(lambda x: dt)
                historical_ndays.append(bhavcopy_df)
            historical_ndays_ls.append(historical_ndays)
        return historical_ndays_ls

    def make_data_plot_ready(self, historical_ndays_df):
        nifty_indices = {}
        for index in ["Nifty 50"]: #self.indices:
            ind = []
            weekly_data = []
            for day in historical_ndays_df:
                dfs = len(day)
                day_n = day[dfs-1].loc[day[dfs-1]['Index Name'].str.lower() == index.lower()]
                day_0 = day[0].loc[day[0]['Index Name'].str.lower() == index.lower()]
                week_date = day_n.loc[0,'Index Date']
                O= day_n.loc[0,'Open Index Value']
                C= day_0.loc[0,'Closing Index Value']
                high = []
                low = []
                for d in day:
                    d = d.loc[d['Index Name'].str.lower() == index.lower()]
                    high.append(d.loc[0,'High Index Value'])
                    low.append(d.loc[0,'Low Index Value'])

                H = max(high)
                L = min(low)
                data = [week_date, O, H, L, C]
                weekly_data.append(data)
            #     day = day.loc[day['Index Name'].str.lower() == index.lower()]
            #     day = day[['Open Index Value', 'High Index Value','Low Index Value','Closing Index Value','Index Date']]
            #     ind.append(day)
            weekly_data = weekly_data[::-1]
            print(*weekly_data)
            df = pd.DataFrame(weekly_data,columns =['Date', 'Open', 'High', 'Low', 'Close'])
            nifty_indices[index] = df
        return nifty_indices

    def generate_graph(self,plot_ready_historical_data):
        
        graph = GenerateDailyGraph(self.graphs_dir)
        for key, index in plot_ready_historical_data.items():
            index.reset_index()
            index['Date'] = pd.DatetimeIndex(index['Date'])
            index = index.set_index('Date')
            index.index.name = 'Date'
            index[["Open", "High","Low","Close"]] = index[["Open", "High","Low","Close"]].apply(pd.to_numeric)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(index.index)
            if self.params.with_ema:
                graph.generate_graph(index, key,emas=self.params.ema)
            else:
                graph.generate_graph(index, key)

    def make_required_dirs(self):
        create_dir(self.reports_dir)
        create_dir(self.graphs_dir)


    def clean_post_report(self):
        remove_files(self.graphs_dir, ext='png')

    def generate_pdf(self):
        generate_pdf(self.reports_dir, self.report_name, self.graphs_dir)

    def process_data(self):        
        # dates = get_n_trading_days(self.params.trading_day)
        # print(len(dates))
        weeks = get_n_trading_weeks(self.params.trading_day)
        historical_ndays_df = self.get_historical_ndays_df(weeks)
        plot_ready_historical_data = self.make_data_plot_ready(historical_ndays_df)
        self.make_required_dirs()
        self.generate_graph(plot_ready_historical_data)
        self.generate_pdf()