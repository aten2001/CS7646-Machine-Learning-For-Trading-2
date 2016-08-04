"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import numpy as np
import scipy.optimize as sco
import math
import sys
sys.path.append("..")
from util import get_data, plot_data
from analysis import get_portfolio_value, get_portfolio_stats


def find_optimal_allocations(prices):
    """Find optimal allocations for a stock portfolio, optimizing for Sharpe ratio.

    Parameters
    ----------
        prices: daily prices for each stock in portfolio

    Returns
    -------
        allocs: optimal allocations, as fractions that sum to 1.0
    """

    # TODO: Your code here
    def statistics(weights):
        start_val=1
        daily_rf=0
        normed=prices/prices.ix[0]
        weights=np.array(weights)
        weights=normed*weights
        pos_val=weights*start_val
        port_val=pos_val.sum(axis=1)
        daily_ret=(port_val/port_val.shift(1))-1
        daily_ret.ix[0]=0
        daily_ret=daily_ret[1:]
        avg_daily_ret=daily_ret.mean()
        std_daily_ret=daily_ret.std()
        sharpe_ratio=math.sqrt(252)*(avg_daily_ret-daily_rf)/std_daily_ret
        return sharpe_ratio
    def min_func_sharpe(allocs):
        return -statistics(allocs)
    noa=prices.shape[1]
    cons=({'type':'eq','fun':lambda x: np.sum(x)-1})
    bnds=tuple((0,1) for x in range(noa))
    result=sco.minimize(min_func_sharpe,noa*[1. / noa,],method='SLSQP',bounds=bnds,constraints=cons,options={'disp': True})
    allocs=result.x
    return allocs


def optimize_portfolio(start_date, end_date, symbols):
    """Simulate and optimize portfolio allocations."""
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get optimal allocations
    allocs = find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations, if they don't sum to 1.0

    # Get daily portfolio value (already normalized since we use default start_val=1.0)
    port_val = get_portfolio_value(prices, allocs)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Optimal allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    normed_SPY = prices_SPY / prices_SPY.ix[0, :]
    df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_data(df_temp, title="Daily Portfolio Value and SPY")


def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['GOOG', 'AAPL', 'GLD', 'HNZ']  # list of symbols
    
    # Optimize portfolio
    optimize_portfolio(start_date, end_date, symbols)


if __name__ == "__main__":
    test_run()
