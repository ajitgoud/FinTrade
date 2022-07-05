from matplotlib.style import available
from compute_daily_data import ComputeDailyData
from download_data import DownloadData
from utils import *
import os

class FinTrade:
    def __init__(self):
        self.today = get_working_day().strftime("%Y%m%d")
        print(self.today)
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.historical_data_dir = os.path.join(self.current_dir, "DailyHistoricalData")

    def check_if_today_bhavcopy_exist(self):
        todays_data_dir = os.path.join(self.historical_data_dir, f'{self.today}.csv')
        return check_if_file_exists(todays_data_dir)
        


if __name__ == "__main__":
    trade = FinTrade()
    
    if not trade.check_if_today_bhavcopy_exist():
        download_data = DownloadData()
        download_data.start_downloading()
    compute = ComputeDailyData(historical_ndays=30)
    compute.compute_nifty_50()
    compute.compute_next_nifty_50()
    compute.compute_mid_150()
    compute.compute_small_250()
    




