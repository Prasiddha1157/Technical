{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "quarterly-somewhere",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import datetime as dt\n",
    "import yfinance as yf\n",
    "import matplotlib.pyplot as plt\n",
    "from pandas_datareader import data as pdr\n",
    "\n",
    "n = 0\n",
    "rsiPeriod = 14\n",
    "maPeriods = [5, 9, 20, 50, 200]\n",
    "\n",
    "yf.pdr_override()\n",
    "\n",
    "# startyear = 2011\n",
    "# startmonth = 1\n",
    "# startday = 2\n",
    "\n",
    "startyear = int(input(\"Enter starting year: \"))\n",
    "startmonth = int(input(\"Enter starting month: \"))\n",
    "startday = int(input(\"Enter starting day: \"))\n",
    "\n",
    "start = dt.datetime(startyear, startmonth, startday)\n",
    "now=dt.datetime.now()\n",
    "\n",
    "class Error(Exception):\n",
    "    pass\n",
    "\n",
    "class InvalidMarket(Error):\n",
    "    pass\n",
    "\n",
    "while True:\n",
    "    try:\n",
    "        market = input(\"Enter a market: \")\n",
    "        market = market.upper()\n",
    "        if market == \"S&P\" or market == \"NASDAQ\" or market == \"SENSEX\" or market == \"HANG SENG\" or market == \"NIKKEI\" or market == \"FTSE\":\n",
    "            stock = input(\"Enter a stock ticker symbol: \")\n",
    "            stock = stock.upper()\n",
    "        else:\n",
    "            raise InvalidMarket\n",
    "        break\n",
    "    except InvalidMarket:\n",
    "        print(\"Market not registered in database. Please enter a registered market.\")\n",
    "        \n",
    "if market == \"S&P\":\n",
    "    df = pd.read_csv('S&P.csv')\n",
    "\n",
    "if market == \"NASDAQ\":\n",
    "    df = pd.read_csv(\"NASDAQ.csv\")\n",
    "    \n",
    "if market == \"FTSE\":\n",
    "    df = pd.read_csv(\"FTSE.csv\")\n",
    "    \n",
    "if market == \"SENSEX\":\n",
    "    df = pd.read_csv(\"SENSEX.csv\")\n",
    "\n",
    "if market == \"NIKKEI\":\n",
    "    df = pd.read_csv(\"NIKKEI.csv\")\n",
    "\n",
    "if market == \"HANG SENG\":\n",
    "    df = pd.read_csv(\"HANGSENG.csv\")\n",
    "    \n",
    "## Now to check if the ticker symbol entered is valid or not.\n",
    "\n",
    "df['Ticker'][n] = df['Ticker'][n].upper()\n",
    "if stock == df['Ticker'][n]:\n",
    "    df_stock = pdr.get_data_yahoo(stock, start, now)\n",
    "    \n",
    "    ## for moving averages\n",
    "    \n",
    "    for x in maPeriods:\n",
    "        ma = x\n",
    "        df_stock['MA_' + str(ma)] = round(df_stock.iloc[:, 4].rolling(window = ma).mean(), 2)\n",
    "        \n",
    "    ## for Moving Average Convergence Divergence (MACD) and Signal Line\n",
    "    \n",
    "    ## short term EMA\n",
    "    \n",
    "    ShortEMA = round(df_stock.iloc[:, 4].ewm(span = 12, adjust = False).mean(), 2)\n",
    "    \n",
    "    ## long term EMA\n",
    "    \n",
    "    LongEMA = round(df_stock.iloc[:, 4].ewm(span = 26, adjust = False).mean(), 2) \n",
    "    \n",
    "    ## MACD line\n",
    "    \n",
    "    MACD = ShortEMA - LongEMA\n",
    "    \n",
    "    ## Signal line\n",
    "    \n",
    "    signal= round(MACD.ewm(span = 9, adjust = False).mean(), 2)\n",
    "    \n",
    "    df_stock['MACD'] = MACD\n",
    "    df_stock['Signal Line'] = signal\n",
    "    \n",
    "    ## for Relative Strength Index\n",
    "    \n",
    "    delta = df_stock['Adj Close'].diff(1)\n",
    "    delta.dropna(inplace = True) ## to drop rows which contain missing values\n",
    "    \n",
    "    positive = delta.copy()\n",
    "    negative = delta.copy()\n",
    "    \n",
    "    positive[positive < 0] = 0\n",
    "    negative[negative > 0] = 0\n",
    "    \n",
    "    avgGain = positive.rolling(window = rsiPeriod).mean()\n",
    "    avgLoss = abs(negative.rolling(window = rsiPeriod).mean()) ## absolute value because we do not want a negative number\n",
    "    \n",
    "    relative_strength = avgGain / avgLoss\n",
    "    RSI = 100.0 - (100.0 / (1.0 + relative_strength))\n",
    "    \n",
    "    df_stock['RSI_14'] = RSI\n",
    "    print(df_stock)\n",
    "    \n",
    "    combined = pd.DataFrame() ## new column with Adj Close and RSI combined\n",
    "    combined['Adj Close'] = df_stock['Adj Close']\n",
    "    combined['RSI'] = RSI\n",
    "    \n",
    "    plt.style.use('fivethirtyeight')\n",
    "    plt.figure(figsize = (25,16))\n",
    "    \n",
    "    ## plotting Adjusted Close\n",
    "    \n",
    "    ax1 = plt.subplot(211) ## number of rows is 2, number of column is 1, and plot number is 1    \n",
    "    ax1.plot(combined.index, combined['Adj Close'], color = 'lightgray') ## looks through every element in the Adj Close column\n",
    "    ax1.set_title(\"Adjusted Close Price\", color = 'white')\n",
    "    \n",
    "    ax1.grid(True, color = '#555555') ## for displaying grid lines\n",
    "    ax1.set_axisbelow(True)\n",
    "    ax1.set_facecolor('black')\n",
    "    ax1.figure.set_facecolor('#121212')\n",
    "    ax1.tick_params(axis = 'x', colors = 'white')\n",
    "    ax1.tick_params(axis = 'y', colors = 'white')\n",
    "    \n",
    "    ## plotting RSI\n",
    "    \n",
    "    ax2 = plt.subplot(212, sharex = ax1)\n",
    "    ax2.plot(combined.index, combined['RSI'], color = 'lightgray')\n",
    "    ax2.axhline(0, linestyle = '--', alpha = 0.5, color = '#ff0000')\n",
    "    ax2.axhline(10, linestyle = '--', alpha = 0.5, color = '#ffaa00')\n",
    "    ax2.axhline(20, linestyle = '--', alpha = 0.5, color = '#00ff00')\n",
    "    ax2.axhline(30, linestyle = '--', alpha = 0.5, color = '#cccccc')\n",
    "    ax2.axhline(70, linestyle = '--', alpha = 0.5, color = '#cccccc')\n",
    "    ax2.axhline(80, linestyle = '--', alpha = 0.5, color = '#00ff00')\n",
    "    ax2.axhline(90, linestyle = '--', alpha = 0.5, color = '#ffaa00')\n",
    "    ax2.axhline(100, linestyle = '--', alpha = 0.5, color = '#ff0000')\n",
    "    \n",
    "    ax2.set_title(\"RSI Value\", color = 'white')\n",
    "    ax2.grid(False) ## for displaying grid lines\n",
    "    ax2.set_axisbelow(True)\n",
    "    ax2.set_facecolor('black')\n",
    "    ax2.tick_params(axis = 'x', colors = 'white')\n",
    "    ax2.tick_params(axis = 'y', colors = 'white')\n",
    "    \n",
    "    plt.show()\n",
    "    \n",
    "    ## plotting MACD and Signal line chart\n",
    "    \n",
    "    plt.figure(figsize = (25, 8))\n",
    "    plt.plot(df_stock.index, MACD, label = stock + \" MACD\", color = 'red')\n",
    "    plt.plot(df_stock.index, signal, label = \"Signal Line\", color = 'blue')\n",
    "    plt.legend(loc = 'upper left')\n",
    "    plt.show()\n",
    "    \n",
    "    \n",
    "while n != len(df['Ticker']):\n",
    "    while stock != df['Ticker'][n]:\n",
    "        n = n+1\n",
    "        df['Ticker'][n] = df['Ticker'][n].upper()\n",
    "        if stock == df['Ticker'][n]:\n",
    "            df_stock = pdr.get_data_yahoo(stock, start, now)\n",
    "            \n",
    "            ## for moving averages\n",
    "            \n",
    "            for x in maPeriods:\n",
    "                ma = x\n",
    "                df_stock['MA_' + str(ma)] = round(df_stock.iloc[:, 4].rolling(window = ma).mean(), 2)\n",
    "                \n",
    "            ## for Moving Average Convergence Divergence (MACD) and Signal Line\n",
    "    \n",
    "            ## short term EMA\n",
    "\n",
    "            ShortEMA = round(df_stock.iloc[:, 4].ewm(span = 12, adjust = False).mean(), 2)\n",
    "\n",
    "            ## long term EMA\n",
    "\n",
    "            LongEMA = round(df_stock.iloc[:, 4].ewm(span = 26, adjust = False).mean(), 2) \n",
    "\n",
    "            ## MACD line\n",
    "\n",
    "            MACD = ShortEMA - LongEMA\n",
    "\n",
    "            ## Signal line\n",
    "\n",
    "            signal= round(MACD.ewm(span = 9, adjust = False).mean(), 2)\n",
    "            \n",
    "            df_stock['MACD'] = MACD\n",
    "            df_stock['Signal Line'] = signal\n",
    "            \n",
    "            ## for RSI \n",
    "            \n",
    "            delta = df_stock['Adj Close'].diff(1)\n",
    "            delta.dropna(inplace = True) ## to drop rows which contain missing values\n",
    "    \n",
    "            positive = delta.copy()\n",
    "            negative = delta.copy()\n",
    "\n",
    "            positive[positive < 0] = 0\n",
    "            negative[negative > 0] = 0\n",
    "\n",
    "            avgGain = positive.rolling(window = rsiPeriod).mean()\n",
    "            avgLoss = abs(negative.rolling(window = rsiPeriod).mean()) ## absolute value because we do not want a negative number\n",
    "\n",
    "            relative_strength = avgGain / avgLoss\n",
    "            RSI = 100.0 - (100.0 / (1.0 + relative_strength))\n",
    "            \n",
    "            df_stock['RSI_14'] = RSI\n",
    "            print(df_stock)\n",
    "\n",
    "            combined = pd.DataFrame() ## new column with Adj Close and RSI combined\n",
    "            combined['Adj Close'] = df_stock['Adj Close']\n",
    "            combined['RSI'] = RSI\n",
    "\n",
    "            plt.figure(figsize = (25,16))\n",
    "\n",
    "            ## plotting Adjusted Close\n",
    "\n",
    "            ax1 = plt.subplot(211) ## number of rows is 2, number of column is 1, and plot number is 1    \n",
    "            ax1.plot(combined.index, combined['Adj Close'], color = 'lightgray') ## looks through every element in the Adj Close column\n",
    "            ax1.set_title(\"Adjusted Close Price\", color = 'white')\n",
    "\n",
    "            ax1.grid(True, color = '#555555') ## for displaying grid lines\n",
    "            ax1.set_axisbelow(True)\n",
    "            ax1.set_facecolor('black')\n",
    "            ax1.figure.set_facecolor('#121212')\n",
    "            ax1.tick_params(axis = 'x', colors = 'white')\n",
    "            ax1.tick_params(axis = 'y', colors = 'white')\n",
    "\n",
    "            ## plotting RSI\n",
    "\n",
    "            ax2 = plt.subplot(212, sharex = ax1)\n",
    "            ax2.plot(combined.index, combined['RSI'], color = 'lightgray')\n",
    "            ax2.axhline(0, linestyle = '--', alpha = 0.5, color = '#ff0000')\n",
    "            ax2.axhline(10, linestyle = '--', alpha = 0.5, color = '#ffaa00')\n",
    "            ax2.axhline(20, linestyle = '--', alpha = 0.5, color = '#00ff00')\n",
    "            ax2.axhline(30, linestyle = '--', alpha = 0.5, color = '#cccccc')\n",
    "            ax2.axhline(70, linestyle = '--', alpha = 0.5, color = '#cccccc')\n",
    "            ax2.axhline(80, linestyle = '--', alpha = 0.5, color = '#00ff00')\n",
    "            ax2.axhline(90, linestyle = '--', alpha = 0.5, color = '#ffaa00')\n",
    "            ax2.axhline(100, linestyle = '--', alpha = 0.5, color = '#ff0000')\n",
    "\n",
    "            ax2.set_title(\"RSI Value\", color = 'white')\n",
    "            ax2.grid(False) ## for displaying grid lines\n",
    "            ax2.set_axisbelow(True)\n",
    "            ax2.set_facecolor('black')\n",
    "            ax2.tick_params(axis = 'x', colors = 'white')\n",
    "            ax2.tick_params(axis = 'y', colors = 'white')\n",
    "\n",
    "            plt.show()\n",
    "\n",
    "            ## plotting MACD and Signal line chart\n",
    "\n",
    "            plt.figure(figsize = (25, 8))\n",
    "            plt.plot(df_stock.index, MACD, label = stock + \" MACD\", color = 'red')\n",
    "            plt.plot(df_stock.index, signal, label = \"Signal Line\", color = 'blue')\n",
    "            plt.legend(loc = 'upper left')\n",
    "            plt.grid(True)\n",
    "            \n",
    "            plt.show()\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "figured-candidate",
   "metadata": {},
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.1"
  },
  "widgets": {
   "application/vnd.jupyter.widget-state+json": {
    "state": {},
    "version_major": 2,
    "version_minor": 0
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
