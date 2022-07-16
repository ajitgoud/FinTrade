from matplotlib.style import available
from compute_daily_data import ComputeDailyData
from download_data import DownloadData
from utils import *
import os
from constant import *

class FnO:
    def __init__(self):
        self.today = get_working_day().strftime("%Y%m%d")
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.historical_data_dir = os.path.join(self.current_dir, HISTORICAL_DATA_DIRNAME)

    def download_bhavcopy(self):
        bhavcopy_dir = os.path.join(self.historical_data_dir, 'fno')
        bhavcopy = os.path.join(bhavcopy_dir, f'{self.today}.csv')
        if not check_if_file_exists(bhavcopy):
            download_bhavcopy = DownloadData(segment=DERIVATIES_SEGMENT,bhavcopy_dir=bhavcopy_dir)
            download_bhavcopy.start_downloading()
        

if __name__ == "__main__":
    fno = FnO()
    fno.download_bhavcopy()
    




