import enum
import os
import pandas as pd
from utils import get_n_trading_days, create_dir,remove_files, get_working_day, check_if_file_exists
import matplotlib.pyplot as plt

class ProcessData:
    def __init__(self, **kwargs):
        self.cols = ['Symbol', 'Instrument', 'Entry date', 'Exit date', 'Weekday',
       'Entry price', 'Exit price', 'Long/Short', 'Position size', 'Stop loss',
       'Profit/Loss', 'Brokerage', 'Days held', 'Set up used',
       'Why this trade?', 'Learnings']
        self.params = kwargs.get('params')
        self.common = kwargs.get('common')
        self.report_name = kwargs.get('report_name')
        self.tradebook_dir = kwargs.get('tradebook_dir')
        self.reports_dir = kwargs.get('reports_dir')
        self.reports_dir = os.path.join(self.reports_dir, self.common.business_date)
        self.graphs_dir = kwargs.get('graphs_dir')

    def read_pnl(self):
        tbook = os.path.join(self.tradebook_dir, "Tradebook.xlsx")
        xls = pd.ExcelFile(tbook)
        pnls ={}
        for sheet in xls.sheet_names:
            print(f'PnL in {sheet}')
            pnl = []
            df = pd.read_excel(xls, sheet, usecols=self.cols)
            df['Exit date'] = pd.to_datetime(df['Exit date']).dt.date
            df = df.groupby(['Exit date'])
            #key.strftime("%d%b%Y")
            for key, item in df:
                pnl.append((key.strftime("%d"), round(item['Profit/Loss'].sum() + item['Brokerage'].sum())))
            
            if len(pnl) > 0:
                pnls[sheet] = pnl[::-1]


        for key, value in pnls.items():
            dt, pnl = map(list, zip(*value))
            print(dt, pnl)

            profits = {'small':0, 'regular':0 , 'medium':0 , 'big':0}
            losses = {'small':0, 'regular':0 , 'medium':0 , 'big':0}
                            

            barls = plt.barh(dt, pnl)
            for i, value in enumerate(pnl):
                if value >= 0:
                    barls[i].set_color('g')
                    if value > 2000:
                        profits['big'] = profits['big'] + 1
                    elif value > 1000:
                        profits['medium'] = profits['medium'] + 1
                    elif value > 500:
                        profits['regular'] = profits['regular'] + 1
                    else:
                        profits['small'] = profits['small'] + 1
                else:
                    barls[i].set_color('r')
                    value = abs(value)
                    if value > 2000:
                        losses['big'] = losses['big'] + 1
                    elif value > 1000:
                        losses['medium'] = losses['medium'] + 1
                    elif value > 500:
                        losses['regular'] = losses['regular'] + 1
                    else:
                        losses['small'] = losses['small'] + 1

            plt.ylabel('Dates')
            plt.xlabel('PnL')
            plt.title(f'{key} PnL')
            plt.savefig(os.path.join(self.reports_dir, f'{key}.png'))
            plt.close()

            temp_key = []
            temp_count = []
            for k, v in profits.items():
                temp_key.append(k)
                temp_count.append(v)
            plt.barh(temp_key, temp_count)
            plt.ylabel('Profit group')
            plt.xlabel('Count')
            plt.title(f'{key} Profits')
            plt.savefig(os.path.join(self.reports_dir, f'{key}-Profit-Count.png'))
            plt.close()

            temp_key = []
            temp_count = []
            for k, v in losses.items():
                temp_key.append(k)
                temp_count.append(v)
            plt.barh(temp_key, temp_count)
            plt.ylabel('Loss group')
            plt.xlabel('Count')
            plt.title(f'{key} Losses')
            plt.savefig(os.path.join(self.reports_dir, f'{key}-Loss-Count.png'))
            plt.close()
            

    def make_required_dirs(self):
        create_dir(self.reports_dir)
        #create_dir(self.graphs_dir)


    def process_data(self):        
        # historical_ndays_df = self.get_historical_ndays_df(dates)
        # self.make_required_dirs()
        # self.generate_graph(plot_ready_historical_data)
        # self.generate_pdf()
        # self.clean_post_report()
        self.make_required_dirs()
        self.read_pnl()

if __name__ == '__main__':
    pnl = ProcessData()
    pnl.read_pnl()