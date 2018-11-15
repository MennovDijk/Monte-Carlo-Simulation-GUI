try:
    # This will work in Python 2.7
    import Tkinter
except ImportError:
    # This will work in Python 3.5
    import tkinter as Tkinter

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data as pdr
from iexfinance import get_historical_data
import fix_yahoo_finance as yf
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

def get_returns_percentages(l):
    n = []
    for i in range(1, len(l)):
        n.append((l[i] - l[i - 1]) / l[i - 1])
    return n


# Define a bold font:
BOLD = ('Garamond', '24', 'bold')

# Create main application window.
root = Tkinter.Tk()

# Create a text box explaining the application.
greeting = Tkinter.Label(text="Monte Carlo Simulation", font=BOLD)
greeting.pack(side='top')

# Create a frame for variable names and entry boxes for their values.
frame = Tkinter.Frame(root)
frame.pack(side='top')

# Variables for the calculation, and default values.
expected_return = Tkinter.StringVar()
expected_return.set('5.00')

num_trading_days = Tkinter.StringVar()
num_trading_days.set('252')

num_simulations = Tkinter.StringVar()
num_simulations.set('10')

ticker = Tkinter.StringVar()
ticker.set('AAPL')

estimation_window_begin = Tkinter.StringVar()
estimation_window_begin.set('2012-01-01')

estimation_window_end = Tkinter.StringVar()
estimation_window_end.set('2018-01-01')

# Creates text boxes and entry boxes for the variables.
row_counter = 0
tkr_text = Tkinter.Label(frame, text='Ticker to analyze:')
tkr_text.grid(row=row_counter, column=0)

tkr_entry = Tkinter.Entry(frame, width=10, textvariable=ticker, justify="center")
tkr_entry.grid(row=row_counter, column=1)

row_counter += 1
er_text = Tkinter.Label(frame, text='Expected Return (in percentages):')
er_text.grid(row=row_counter, column=0)

er_entry = Tkinter.Entry(frame, width=10, textvariable=expected_return, justify="center")
er_entry.grid(row=row_counter, column=1)

row_counter += 1
beg_text = Tkinter.Label(frame, text='Begin date of the estimation window:')
beg_text.grid(row=row_counter, column=0)

beg_entry = Tkinter.Entry(frame, width=10, textvariable=estimation_window_begin, justify="center")
beg_entry.grid(row=row_counter, column=1)

row_counter += 1
end_text = Tkinter.Label(frame, text='End date of the estimation window:')
end_text.grid(row=row_counter, column=0)

end_entry = Tkinter.Entry(frame, width=10, textvariable=estimation_window_end, justify="center")
end_entry.grid(row=row_counter, column=1)

row_counter += 1
nss_text = Tkinter.Label(frame, text='Number of stock simulations to run:')
nss_text.grid(row=row_counter, column=0)

nss_entry = Tkinter.Entry(frame, width=10, textvariable=num_simulations, justify="center")
nss_entry.grid(row=row_counter, column=1)

row_counter += 1
ntd_text = Tkinter.Label(frame, text='Number of trading days to analyze:')
ntd_text.grid(row=row_counter, column=0)

ntd_entry = Tkinter.Entry(frame, width=10, textvariable=num_trading_days, justify="center")
ntd_entry.grid(row=row_counter, column=1)

# Define a function to create the desired plot.
def make_plot(event=None):
    # Get these variables from outside the function, and update them.
    global expected_return, num_trading_days, num_simulations, estimation_window_begin, estimation_window_end

    # Convert StringVar data to numerical data.
    mu = float(expected_return.get())/100
    N = int(num_trading_days.get())
    K = int(num_simulations.get())
    stock = str(ticker.get())
    begin =  datetime.datetime.strptime(str(estimation_window_begin.get()), '%Y-%m-%d')
    end = datetime.datetime.strptime(str(estimation_window_begin.get()), '%Y-%m-%d')

    yf.pdr_override()
    stock_data = pdr.get_data_yahoo(stock, begin, end)

    stock_data.reset_index(inplace=True, drop=False)

    sigma = np.std(get_returns_percentages(stock_data['Adj Close'])) * np.sqrt(252)  # std dev over total interval

    S1 = list(stock_data['Adj Close'])[-1]  # initial capital ($)
    dt = sigma / np.sqrt(N)

    for k in range(0, K):
        St = [S1]
        for i in range(1, N + 1):
            eps = np.random.normal()
            S = St[i - 1] + (St[i - 1] * (mu * dt + sigma * eps * np.sqrt(dt)))
            St.append(S)
        plt.plot(St)

    # Create the plot.
    patch_sigma = mpatch.Patch(color='blue', label='Standard Deviation over Interval = ' + str((round(sigma,4)*100))+"%")
    patch_expected_return = mpatch.Patch(color='red', label='Expected Return = ' + str(expected_return.get())+ "%")
    plt.xlabel('Total Amount of Trading Days')
    plt.ylabel('Stock Price')
    plt.title('Ticker = ' + stock)
    plt.legend(handles=[patch_sigma, patch_expected_return])
    plt.show()


# Add a button to create the plot.
MakePlot = Tkinter.Button(root, command=make_plot, text="Create Plots")
MakePlot.pack(side='bottom', fill='both')

# Allow pressing <Return> to create plot.
root.bind('<Return>', make_plot)

root.wm_title("Monte Carlo Simulation")
# Activate the window.
root.mainloop()



# thedate = datetime.datetime.strptime(userdatestring, '%Y-%m-%d')