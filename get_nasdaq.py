import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf

import pandas_datareader.data as web 
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import tqdm
import pyperclip

symbols = get_nasdaq_symbols()
symbols.head()

cnt = 0

nasdaqs = ""
path = "src/nasdaq.txt"

with open(path, mode="w") as file:
    for s in (symbols.index):
        # cnt += 1
        # if cnt == 10:
        #     break
        try:
            file.write('\"'+s+'\"'+","+'\n')
            print('\"'+s+'\"')
        except:
            print("error",s)

    print("finish")

    pyperclip.copy(nasdaqs)