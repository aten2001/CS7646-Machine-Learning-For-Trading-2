You are given the following inputs for analyzing a portfolio:

A date range to select the historical data to use (specified by a start and end date)
Symbols for equities (e.g., GOOG, AAPL, GLD, XOM)
Allocations to the equities at the beginning of the simulation (e.g., 0.2, 0.3, 0.4, 0.1)
Total starting value of the portfolio (e.g. $1,000,000)
Your goal is to compute the daily portfolio value over given date range, and then the following statistics for the overall portfolio:

Cumulative return
Average daily return
Standard deviation of daily returns
Sharpe ratio of the overall portfolio, given daily risk free rate (usually 0), and yearly sampling frequency (usually 252, the no. of trading days in a year)
Your program will include a helper function to specify the portfolio data, then your function should calculate and return the portfolio statistics. Be sure to include all necessary code in your submitted Python code. For grading purposes, we will test ONLY the function that computes statistics. You should implement the following API EXACTLY, if you do not your submission will be penalized at least 20%.

import datetime as dt
cr, adr, sddr, sr, ev = \
    assess_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0, sf=252)
Where the returned outputs are:

cr: Cumulative return
adr: Average daily return
sddr: Standard deviation of daily return
ev: End value of portfolio
The input parameters are:

sd: A datetime object that represents the start date
ed: A datetime object that represents the end date
syms: A list of symbols that make up the portfolio (note that your code should support any symbol in the data directory)
allocs: A list of allocations to the stocks, must sum to 1.0
sv: Start value of the portfolio
rfr: The risk free rate for the entire period
sf: Sampling frequency per year
