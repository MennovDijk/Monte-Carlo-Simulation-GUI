try:
    # This will work in Python 2.7
    import Tkinter
except ImportError:
    # This will work in Python 3.5
    import tkinter as Tkinter
from pandas_datareader import data
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
def get_returns_percentages(l):
    n = []
    for i in range(1, len(l)):
        n.append((l[i] - l[i - 1]) / l[i - 1])
    return n


# Define a bold font:
BOLD = ('Palatino', '24', 'bold')

# Create main application window.
root = Tkinter.Tk()

# Create a text box explaining the application.
greeting = Tkinter.Label(text="Monte Carlo Simulation", font=BOLD)
greeting.pack(side='top')

# Create a frame for variable names and entry boxes for their values.
frame = Tkinter.Frame(root)
frame.pack(side='top')

# Variables for the calculation, and default values.
Expected_Return = Tkinter.StringVar()
Expected_Return.set('5.00')

num_trading_days = Tkinter.StringVar()
num_trading_days.set('252')

num_simulations = Tkinter.StringVar()
num_simulations.set('10')

ticker = Tkinter.StringVar()
ticker.set('AAPL')

# Create text boxes and entry boxes for the variables.
# Use grid geometry manager instead of packing the entries in.
row_counter = 0
tkr_text = Tkinter.Label(frame, text='Ticker to analyze:')
tkr_text.grid(row=row_counter, column=0)

nss_entry = Tkinter.Entry(frame, width=8, textvariable=ticker)
nss_entry.grid(row=row_counter, column=1)

row_counter += 1
er_text = Tkinter.Label(frame, text='Expected Return (in percentages):')
er_text.grid(row=row_counter, column=0)

er_entry = Tkinter.Entry(frame, width=8, textvariable=Expected_Return)
er_entry.grid(row=row_counter, column=1)

row_counter += 1
nss_text = Tkinter.Label(frame, text='Number of stock simulations to run:')
nss_text.grid(row=row_counter, column=0)

nss_entry = Tkinter.Entry(frame, width=8, textvariable=num_simulations)
nss_entry.grid(row=row_counter, column=1)

row_counter += 1
ntd_text = Tkinter.Label(frame, text='Number of trading days to analyze:')
ntd_text.grid(row=row_counter, column=0)

ntd_entry = Tkinter.Entry(frame, width=8, textvariable=num_trading_days)
ntd_entry.grid(row=row_counter, column=1)

# Define a function to create the desired plot.
def make_plot(event=None):
    # Get these variables from outside the function, and update them.
    global Expected_Return, num_trading_days, num_simulations

    # Convert StringVar data to numerical data.
    mu = float(Expected_Return.get())/100
    N = int(num_trading_days.get())
    K = int(num_simulations.get())
    stock = str(ticker.get())

    start = datetime.datetime(2012, 1, 1)
    end = datetime.datetime(2017, 1, 1)

    stock_data = data.DataReader(stock, 'yahoo', start, end)
    stock_data.reset_index(inplace=True, drop=False)

    sigma = np.std(get_returns_percentages(stock_data['Adj Close'])) * math.sqrt(252)  # std dev over total interval
    S1 = list(stock_data['Adj Close'])[-1]  # initial capital ($)
    dt = sigma / math.sqrt(N)

    for k in range(0, K):
        St = [S1]
        for i in range(1, N + 1):
            eps = np.random.normal()
            S = St[i - 1] + (St[i - 1] * (mu * dt + sigma * eps * math.sqrt(dt)))
            St.append(S)
        plt.plot(St)

    # Create the plot.
    patch_sigma = mpatch.Patch(color='blue', label='Standard Deviation over Interval = ' + str((round(sigma,4)*100))+"%")
    patch_expected_return = mpatch.Patch(color='red', label='Expected Return = ' + str(Expected_Return.get())+ "%")
    plt.xlabel('Total Amount of Trading Days')
    plt.ylabel('Stock Price')
    plt.title('Ticker = ' + stock)
    plt.legend(handles=[patch_sigma, patch_expected_return])
    plt.show()


# Add a button to create the plot.
MakePlot = Tkinter.Button(root, command=make_plot, text="Create Plot")
MakePlot.pack(side='bottom', fill='both')

# Allow pressing <Return> to create plot.
root.bind('<Return>', make_plot)

root.wm_title("Monte Carlo Simulation")
# Activate the window.
root.mainloop()