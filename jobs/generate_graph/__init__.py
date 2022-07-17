import os
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta

from requests import session


class GenerateDailyGraph:
    def __init__(self, chart_save_dir, emas):
        self.chart_save_dir = chart_save_dir
        self.emas = emas


    def generate_graph(self, stock, title, show_volume=False):  
        title = f"{title}.png"
        if show_volume:
            volplot = mpf.make_addplot(stock['Volume'].rolling(window=20).mean(), width=0.8, panel=1,color='b')
            self.plot_daily_chart(stock, title,volplot)
        else:
            self.plot_daily_chart_without_vol(stock, title)
        #self.invest(stock, title)
        # for session, ema in self.emas.items():
        #    self.plot_ema_chart(stock, title, volplot, ema[0], ema[1])


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
        elif e9>e21:
            if e25>e50:
                if e50>e100:
                    if e100>e200:
                        print(f'{title} is Perfect')
                    else:
                        print(f'{title} is e200>e100')
                else:
                    print(f'{title} is e100>e50')
            else:
                print(f'{title} is e50>e25')

    def plot_ema_chart(self,stock, title, volplot,span1=9, span2=21):
        sub_dir = f'ema_{span1}_{span2}'
        fig_path = os.path.join(self.chart_save_dir, sub_dir, title)
        e1_df = stock['Close'].ewm(span=span1, adjust=False).mean()
        e2_df = stock['Close'].ewm(span=span2, adjust=False).mean()
        e1_close = round(e1_df.iloc[-1], 2)
        e2_close = round(e2_df.iloc[-1], 2)
        stock_close = round(stock["Close"].iloc[-1],2)
        long_crossover = e1_close > e2_close
        stock_above = stock_close > e1_close if long_crossover else False
        e1 = mpf.make_addplot(e1_df,width=0.9, color='forestgreen')
        e2 = mpf.make_addplot(e2_df,width=0.9, color='indigo')
        addplots = [e1, e2,volplot]
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,addplot=addplots, volume=True, figratio=(16,9), savefig=fig_path)

    def plot_daily_chart(self,stock, title,volplot):
        graph_file = os.path.join(self.chart_save_dir,title)
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,addplot=volplot, volume=True, figratio=(16,9), savefig=graph_file)
        
    def plot_daily_chart_without_vol(self,stock, title):
        graph_file = os.path.join(self.chart_save_dir,title)
        mpf.plot(stock,type='candle',style='yahoo',title=title, figscale=1.5,figratio=(16,9), savefig=graph_file)
        