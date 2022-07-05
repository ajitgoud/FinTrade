import pandas as pd
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
nifty_500_file_name = "nifty_500.csv"
nifty_500_file_path =  os.path.join(dir_path, "DailyHistoricalData", nifty_500_file_name)
print(nifty_500_file_path)