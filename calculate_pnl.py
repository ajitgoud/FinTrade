from traceback import print_last
import pandas as pd

class PnL:
    def __init__(self):
        self.cols = ['Symbol', 'Instrument', 'Entry date', 'Exit date', 'Weekday',
       'Entry price', 'Exit price', 'Long/Short', 'Position size', 'Stop loss',
       'Profit/Loss', 'Brokerage', 'Days held', 'Set up used',
       'Why this trade?', 'Learnings']

    def read_pnl(self):
        filename = 'D:\_Learnings\Career\Share market\FinTrade\PnL\Tradebook.xlsx'
        xls = pd.ExcelFile(filename)
        df1 = pd.read_excel(xls, 'JUN-22', usecols=self.cols)
        # df2 = pd.read_excel(xls, 'JUL-22', usecols=self.cols)
        # df1 = df1.dropna()
        print(df1['Exit date'])
        d = df1.groupby(['Exit date'])
        print(d)
        # df2 = df2.dropna()
        # print(df2)
        for key, item in d:
            print(round(item['Profit/Loss'].sum() + item['Brokerage'].sum()))

if __name__ == '__main__':
    pnl = PnL()
    pnl.read_pnl()