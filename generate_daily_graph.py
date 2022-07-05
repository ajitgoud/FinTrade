import os
import pandas as pd
import mplfinance as mpf
from datetime import datetime, date, timedelta


class GenerateDailyGraph:
    def __init__(self):
        pass

    def generate_graph(self, stock, title, chart_save_path):  
        title = f"{title}.png"  
        chart_save_path = os.path.join(chart_save_path, title)
        mpf.plot(stock,type='candle',style='yahoo',title=title, volume=True, figratio=(16,9), savefig=chart_save_path)