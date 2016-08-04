"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os
import datetime as dt
from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """
    # TODO: Your code here
    startDate=dt.datetime.strptime(start_date, "%Y-%m-%d")
    endDate=dt.datetime.strptime(end_date, "%Y-%m-%d")
    symbols=set()
    df_orders=pd.read_csv(orders_file)


    dates=pd.date_range(startDate,endDate)
    df_price=pd.DataFrame(index=dates)
    num=len(df_orders['Symbol'])
    for symbol in df_orders['Symbol']:
         symbols.add(symbol)

    for symbol in symbols:
         df_temp=pd.read_csv("data/{}.csv".format(symbol),index_col='Date',parse_dates=True,usecols=['Date','Adj Close'],na_values=['nan'])
         df_temp=df_temp.rename(columns={'Adj Close':symbol})
         df_price=df_price.join(df_temp)
         df_price=df_price.fillna(method="ffill")

    df_trade = pd.DataFrame(index=dates, columns=symbols)
    df_trade= df_trade.fillna(0)
    for i in range(num):
        df_orders['Date'][i]=dt.datetime.strptime(df_orders['Date'][i],"%Y-%m-%d")
        for d in dates:
            if d==df_orders['Date'][i]:
                symbol=df_orders['Symbol'][i]
                if df_orders['Order'][i]=="BUY":
                    df_trade[symbol][d]=df_trade[symbol][d]+int(df_orders['Shares'][i])
                elif df_orders['Order'][i]=="SELL":
                    df_trade[symbol][d]=df_trade[symbol][d]-int(df_orders['Shares'][i])

    df_trade_abs=abs(df_trade)

    df_holding = pd.DataFrame(index=dates, columns=symbols)
    df_holding= df_holding.fillna(0)
    for s in symbols:
        df_holding[s][dates[0]]=df_trade[s][dates[0]]
        for i in range(1,len(dates)):
            df_holding[s][dates[i]]=df_trade[s][dates[i]]+df_holding[s][dates[i-1]]


    df_holding_value=df_holding*df_price

    df_holding_value=df_holding_value.dropna()
    df_total_holding=df_holding_value.sum(axis=1)

    column=['cash']
    df_value=pd.DataFrame(index=dates)
    df_value=df_trade*df_price
    df_value_abs=df_trade_abs*df_price
    df_value_abs_total=df_value_abs.sum(axis=1)
    df_use_abs=pd.DataFrame(index=dates, columns=column)
    df_use_abs=df_use_abs.fillna(0.00)
    df_temp1=df_value_abs.sum(axis=1)
    for d in dates:
        df_use_abs['cash'][d]=df_temp1[d]

    df_use=pd.DataFrame(index=dates, columns=column)
    df_use=df_use.fillna(0.00)
    df_temp2=df_value.sum(axis=1)
    for d in dates:
        df_use['cash'][d]=df_temp2[d]

    column=['cash']
    df_cash=pd.DataFrame(index=dates, columns=column)

    df_cash=df_cash.fillna(0.00)

    df_cash['cash'][dates[0]]=start_val-df_use['cash'][dates[0]]


    for i in range(1,len(dates)):
        df_cash['cash'][dates[i]]=df_cash['cash'][dates[i-1]]-df_use['cash'][dates[i]]


    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    df_portval=df_total_holding+df_cash

    portvals=pd.DataFrame(index=prices_SPX.index)
    portvals=portvals.join(df_portval)

    return portvals

def leverage(start_date, end_date, orders_file, start_val):
    startDate=dt.datetime.strptime(start_date, "%Y-%m-%d")
    endDate=dt.datetime.strptime(end_date, "%Y-%m-%d")
    symbols=set()
    df_orders=pd.read_csv(orders_file)


    dates=pd.date_range(startDate,endDate)
    df_price=pd.DataFrame(index=dates)
    num=len(df_orders['Symbol'])
    for symbol in df_orders['Symbol']:
         symbols.add(symbol)

    for symbol in symbols:
         df_temp=pd.read_csv("data/{}.csv".format(symbol),index_col='Date',parse_dates=True,usecols=['Date','Adj Close'],na_values=['nan'])
         df_temp=df_temp.rename(columns={'Adj Close':symbol})
         df_price=df_price.join(df_temp)
         df_price=df_price.fillna(method="ffill")

    df_trade = pd.DataFrame(index=dates, columns=symbols)
    df_trade= df_trade.fillna(0)
    for i in range(num):
        df_orders['Date'][i]=dt.datetime.strptime(df_orders['Date'][i],"%Y-%m-%d")
        for d in dates:
            if d==df_orders['Date'][i]:
                symbol=df_orders['Symbol'][i]
                if df_orders['Order'][i]=="BUY":
                    df_trade[symbol][d]=df_trade[symbol][d]+int(df_orders['Shares'][i])
                elif df_orders['Order'][i]=="SELL":
                    df_trade[symbol][d]=df_trade[symbol][d]-int(df_orders['Shares'][i])

    df_trade_abs=abs(df_trade)

    df_holding = pd.DataFrame(index=dates, columns=symbols)
    df_holding= df_holding.fillna(0)
    for s in symbols:
        df_holding[s][dates[0]]=df_trade[s][dates[0]]
        for i in range(1,len(dates)):
            df_holding[s][dates[i]]=df_trade[s][dates[i]]+df_holding[s][dates[i-1]]


    df_holding_value=df_holding*df_price
    df_holding_value=df_holding_value.dropna()
    df_total_holding=df_holding_value.sum(axis=1)

    df_longs = pd.DataFrame(index=dates, columns=symbols)
    df_longs= df_longs.fillna(0.00)
    for s in symbols:
        for i in range(len(dates)):
            if df_holding_value[s][dates[i]]>0:
                df_longs[s][dates[i]]=df_holding_value[s][dates[i]]
    df_longs_total=df_longs.sum(axis=1)
    df_shorts = pd.DataFrame(index=dates, columns=symbols)
    df_shorts= df_shorts.fillna(0.00)
    for s in symbols:
        for i in range(len(dates)):
            if df_holding_value[s][dates[i]]<0:
                df_shorts[s][dates[i]]=df_holding_value[s][dates[i]]
    df_shorts_total=df_shorts.sum(axis=1)
    df_shorts_total_abs=abs(df_shorts_total)


    column=['cash']
    df_value=pd.DataFrame(index=dates)
    df_value=df_trade*df_price
    df_value_abs=df_trade_abs*df_price
    df_value_abs_total=df_value_abs.sum(axis=1)
    df_use_abs=pd.DataFrame(index=dates, columns=column)
    df_use_abs=df_use_abs.fillna(0.00)
    df_temp1=df_value_abs.sum(axis=1)
    for d in dates:
        df_use_abs['cash'][d]=df_temp1[d]

    df_use=pd.DataFrame(index=dates, columns=column)
    df_use=df_use.fillna(0.00)
    df_temp2=df_value.sum(axis=1)
    for d in dates:
        df_use['cash'][d]=df_temp2[d]

    column=['cash']
    df_cash=pd.DataFrame(index=dates, columns=column)

    df_cash=df_cash.fillna(0.00)

    df_cash['cash'][dates[0]]=start_val-df_use['cash'][dates[0]]


    for i in range(1,len(dates)):
        df_cash['cash'][dates[i]]=df_cash['cash'][dates[i-1]]-df_use['cash'][dates[i]]

    df_leverage=(df_longs_total+df_shorts_total_abs)/((df_longs_total-df_shorts_total_abs)+df_cash['cash'])

    df_trade_temp=df_trade
    for i in range(len(dates)):
        if df_leverage[dates[i]]>2.0:
            for s in symbols:
                for s in symbols:
                    df_trade[s][dates[i]]=0
                df_holding[s][dates[i]]=df_trade_temp[s][dates[i]]+df_holding[s][dates[i-1]]
                df_holding_value=df_holding*df_price
                df_total_holding=df_holding_value.sum(axis=1)
                if df_holding_value[s][dates_range[i]]>0:
                    df_longs[s][dates[i]]=df_holding_value[s][dates[i]]
                df_longs_total=df_longs.sum(axis=1)
                if df_holding_value[s][dates_range[i]]<0:
                    df_shorts[s][dates[i]]=df_holding_value[s][dates[i]]
                df_shorts_total=df_shorts.sum(axis=1)
                df_shorts_total_abs=abs(df_shorts_total)
                df_value=df_trade*df_price
                df_use=df_value.sum(axis=1)
                df_cash['cash'][dates[0]]=startval-df_use['cash'][dates[0]]
                df_cash['cash'][dates[i]]=df_cash['cash'][dates[i-1]]-df_use['cash'][dates[i]]
                df_leverage=(df_longs_total+df_shorts_total_abs)/((df_longs_total-df_shorts_total_abs)+df_cash['cash'])
                if df_leverage[dates[i]]>2.0:
                    df_holding[s][dates[i]]=df_trade[s][dates[i]]+df_holding[s][dates[i-1]]
                    df_holding_value=df_holding*df_price
                    df_total_holding=df_holding_value.sum(axis=1)
                    if df_holding_value[s][dates_range[i]]>0:
                        df_longs[s][dates[i]]=df_holding_value[s][dates[i]]
                    df_longs_total=df_longs.sum(axis=1)
                    if df_holding_value[s][dates_range[i]]<0:
                        df_shorts[s][dates[i]]=df_holding_value[s][dates[i]]
                    df_shorts_total=df_shorts.sum(axis=1)
                    df_shorts_total_abs=abs(df_shorts_total)
                    df_value=df_trade*df_price
                    df_use=df_value.sum(axis=1)
                    df_cash['cash'][dates[0]]=startval-df_use['cash'][dates[0]]
                    df_cash['cash'][dates[i]]=df_cash['cash'][dates[i-1]]-df_use['cash'][dates[i]]
                    df_leverage=(df_longs_total+df_shorts_total_abs)/((df_longs_total-df_shorts_total_abs)+df_cash['cash'])

    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    df_portval=df_total_holding+df_cash
    portvals=pd.DataFrame(index=prices_SPX.index)
    portvals=portvals.join(df_portval)
    return portvals

def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2011-1-14'
    end_date = '2011-12-14'
    orders_file = os.path.join("orders", "orders2.csv")
    start_val = 1000000

    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])



if __name__ == "__main__":
    test_run()
