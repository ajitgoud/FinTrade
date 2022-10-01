import os
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta

from requests import session


class GenerateDailyGraph:
    def __init__(self, chart_save_dir):
        self.chart_save_dir = chart_save_dir


    def generate_graph(self, stock, title, show_volume=False, emas=None):  
        title = f"{title}.png"
        if emas:
            if show_volume:
                volplot = mpf.make_addplot(stock['Volume'].rolling(window=20).mean(), width=0.8, panel=1,color='b')
                self.plot_ema_chart(stock, title, emas, show_volume=True, vol_plot=volplot)
            else:
                self.plot_ema_chart(stock, title,emas)
        elif show_volume:
            volplot = mpf.make_addplot(stock['Volume'].rolling(window=20).mean(), width=0.8, panel=1,color='b')
            self.plot_daily_chart(stock, title, volplot)
        else:
            self.plot_daily_chart_without_vol(stock, title)

        #self.invest(stock, title)
        # for session, ema in self.emas.items():
        #    self.plot_ema_chart(stock, title, volplot, ema[0], ema[1])

    def plot_ema_chart(self,stock, title, emas, show_volume=False, vol_plot=None):
        graph_file = os.path.join(self.chart_save_dir,title)
        colors = ['forestgreen', 'indigo', 'navy', 'maroon']
        addplots = []
        for i, ema in enumerate(emas):
            df = stock['Close'].ewm(span=ema, adjust=False).mean()
            e = mpf.make_addplot(df,width=0.9, color=colors[i])
            addplots.append(e)
        if show_volume and vol_plot:
            addplots.append(vol_plot)
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,addplot=addplots, volume=show_volume, figratio=(16,9), savefig=graph_file)


    def invest(self,stock, title):
        e9_df = stock['Close'].ewm(span=9, adjust=False).mean()
        e21_df = stock['Close'].ewm(span=21, adjust=False).mean()
        e25_df = stock['Close'].ewm(span=25, adjust=False).mean()
        e50_df = stock['Close'].ewm(span=50, adjust=False).mean()
        e100_df = stock['Close'].ewm(span=100, adjust=False).mean()
        e200_df = stock['Close'].ewm(span=200, adjust=False).mean()

        e9 = round(e9_df.iloc[-1], 2)
        e21 = round(e21_df.iloc[-1], 2)
        e25 = round(e25_df.iloc[-1], 2)
        e50 = round(e50_df.iloc[-1], 2)
        e100 = round(e100_df.iloc[-1], 2)
        e200 = round(e200_df.iloc[-1], 2)
        stock_close = round(stock["Close"].iloc[-1],2)

        if stock_close > e200:
            print(f'{title} is Above 200 EMA')
        

    def plot_daily_chart(self,stock, title,volplot):
        graph_file = os.path.join(self.chart_save_dir,title)
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,addplot=volplot, volume=True, figratio=(16,9), savefig=graph_file)
        
    def plot_daily_chart_without_vol(self,stock, title):
        graph_file = os.path.join(self.chart_save_dir,title)
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,figratio=(16,9), savefig=graph_file)