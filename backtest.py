from utils import *

import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.test import SMA
from backtesting.lib import crossover

# sample backtest to demonstrate the use of the backtesting library

if __name__ == '__main__':
    
    df = get_data('GOOG', period='4y')

    df.ta.ema(length=50, append=True)
    df.ta.ema(length=200, append=True)
    #df.ta.rsi(length=14, append=True)

    df.dropna(inplace=True)

    df = df.loc[:'2025-01-31']
    #print(df.info())


    class SampleStrat(Strategy):

        def init(self):
            self.ema50 = self.I(lambda: self.data.EMA_50, name='EMA_50')
            self.ema200 = self.I(lambda: self.data.EMA_200, name='EMA_200')

            #self.rsi14 = self.I(lambda: self.data.RSI_14, name='RSI_14')

        def next(self):
            if crossover(self.ema50, self.ema200):
                self.buy()

            elif crossover(self.ema200, self.ema50):
                self.sell()


    bt = Backtest(df, SampleStrat, exclusive_orders=True, finalize_trades=True)
    results = bt.run()

    print(results)  
    bt.plot()
