__author__ = 'shinshaw'
__author__ = 'shinshaw'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import KNNLearner as knn
import sys

def write():
    name='orders/myorder.csv'
    try:
        file1 = open(name,'a')
        file1.write('Date'+',')
        file1.write('Symbol'+',')
        file1.write('Order'+',')
        file1.write('Shares')
        file1.close()
    except:
        print('Something went wrong!')
        sys.exit(0)

def loadDataSet(filename,start_date,end_date):
    dates=pd.date_range(start_date,end_date)
    df=pd.DataFrame(index=dates)
    df_file=pd.read_csv(filename,index_col="Date",parse_dates=True,usecols=['Date','Adj Close'],na_values=['nan'])
    df=df.join(df_file)
    df=df.dropna()
    return df

def get_data_all(filename,start_date,end_date):
    dates=pd.date_range(start_date,end_date)
    df=pd.DataFrame(index=dates)
    df_file=pd.read_csv(filename,index_col="Date",parse_dates=True,na_values=['nan'])
    df=df.join(df_file)
    df=df.dropna()
    return df

def training(df):
    trainY=(df.shift(-5)/df)-1
    trainY=trainY.rename(columns={'Adj Close':'trainY'})
    return trainY


def bollinger_band(df, window):
    rm=pd.rolling_mean(df['Adj Close'], window=window)
    rstd=pd.rolling_std(df['Adj Close'],window=window)
    df_BV=(df-rm)/(2*rstd)
    df_BV=df_BV.rename(columns={'Adj Close':'BV'})
    return df_BV

def MAC(df,window1,window2):
    ma_12 = pd.rolling_mean(df['Adj Close'], window=window1)
    ma_26 = pd.rolling_mean(df['Adj Close'], window=window2)
    df_MAC=df.copy(deep=True)
    for d in df.index[0:]:
        t_entry=pd.Timestamp(d)
        loc_entry=df.index.get_loc(t_entry)
        df_MAC['Adj Close'].iloc[loc_entry]=(ma_12.iloc[loc_entry]-ma_26.iloc[loc_entry])/ma_26.iloc[loc_entry]
    df_MAC=df_MAC.rename(columns={'Adj Close':'MACD'})
    return df_MAC

def RSI(df,df1, n):
    i = 0
    HighI = [0]
    LowI = [0]
    while i + 1 <= df.index[-1]:
        HighMove = df.get_value(i + 1, 'High') - df.get_value(i, 'High')
        LowMove = df.get_value(i, 'Low') - df.get_value(i + 1, 'Low')
        if HighMove > LowMove and HighMove > 0:
            HighD = HighMove
        else: HighD = 0
        HighI.append(HighD)
        if LowMove > HighMove and LowMove > 0:
            LowD = LowMove
        else: LowD = 0
        LowI.append(LowD)
        i = i + 1
    UpI = pd.Series(HighI)
    DoI = pd.Series(LowI)
    Pos = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1))
    Neg = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1))
    RS = pd.Series((Pos+Neg) / Neg, name = 'RSI_' + str(n))
    RSI=(100-(100/RS))/100
    df_rsi=df1.copy(deep=True)
    for d in df_rsi.index[0:]:
        t_entry=pd.Timestamp(d)
        loc_entry=df_rsi.index.get_loc(t_entry)
        df_rsi['Adj Close'].iloc[loc_entry]=RSI[loc_entry]

    df_rsi=df_rsi.rename(columns={'Adj Close':'RSI'})
    return df_rsi

def order(df,symbol,ax,index):
    for d in df.index[index:]:
        t_entry=pd.Timestamp(d)
        loc_entry=df.index.get_loc(t_entry)
        ymin, ymax = ax.get_ylim()
        if df['Adj Close'].iloc[loc_entry]>1.03:
            ax.vlines(x=d, ymin=ymin, ymax=ymax-1,color='g')
            f=open('orders/myorder.csv','ab+')
            d=d.date()
            date=str(d)
            f.write('\n'+date+',')
            f.write(symbol+',')
            f.write('BUY'+',')
            f.write('100')
            for d1 in df.index[loc_entry+1:]:
                t_exit=pd.Timestamp(d1)
                loc_exit=df.index.get_loc(t_exit)
                if df['Adj Close'].iloc[loc_exit]<0.97:
                    loc_exit=loc_exit+5
                    if loc_exit>df.size:
                        break
                    d1=df.index[loc_exit]
                    ax.vlines(x=d1, ymin=ymin, ymax=ymax-1,color='k')
                    f=open('orders/myorder.csv','ab+')
                    d1=d1.date()
                    date=str(d1)
                    f.write('\n'+date+',')
                    f.write(symbol+',')
                    f.write("SELL"+',')
                    f.write("100")
                    order(df,symbol,ax,loc_exit)
                    break
            break
        if df['Adj Close'].iloc[loc_entry]<0.97:
            ax.vlines(x=d, ymin=ymin, ymax=ymax-1,color='r')
            f=open('orders/myorder.csv','ab+')
            d=d.date()
            date=str(d)
            f.write('\n'+date+',')
            f.write(symbol+',')
            f.write('SELL'+',')
            f.write('100')
            for d1 in df.index[loc_entry+1:]:
                t_exit=pd.Timestamp(d1)
                loc_exit=df.index.get_loc(t_exit)
                if df['Adj Close'].iloc[loc_exit]>1.03:
                    loc_exit=loc_exit+5
                    if loc_exit>df.size:
                        break
                    d1=df.index[loc_exit]
                    ax.vlines(x=d1, ymin=ymin, ymax=ymax-1,color='k')
                    f=open('orders/myorder.csv','ab+')
                    d1=d1.date()
                    date=str(d1)
                    f.write('\n'+date+',')
                    f.write(symbol+',')
                    f.write("BUY"+',')
                    f.write("100")
                    order(df,symbol,ax,loc_exit)
                    break
            break
def test_run():
    df=loadDataSet("data/IBM.csv",'2007-12-31','2009-12-31')

    trainingY=training(df)
    trainingY=trainingY.dropna()
    trainY_before=(df.shift(-5)/df)
    trainY_before=df['Adj Close']*trainY_before
    trainY_before=trainY_before.dropna()

    df1=get_data_all("data/IBM.csv",'2007-12-31','2009-12-31')
    df1=df1.reset_index()
    mac=MAC(df,12,26)
    mac=mac.dropna()
    rsi=RSI(df1,df,14)
    rsi=rsi.dropna()
    bv=bollinger_band(df, 20)
    bv=bv.dropna()
    dates=pd.date_range('2007-12-31','2009-12-31')
    df_data_train=pd.DataFrame(index=dates)
    df_data_train=df_data_train.join(bv,how='inner')
    df_data_train=df_data_train.join(mac,how='inner')
    df_data_train=df_data_train.join(rsi,how='inner')
    df_data_train=df_data_train.join(trainingY,how='inner')
    df_test=loadDataSet("data/IBM.csv",'2009-12-31','2010-12-31')

    trainingY_test=training(df_test)
    trainingY_test=trainingY_test.dropna()
    trainY_after=(df_test.shift(-5)/df_test)
    trainY_after=df_test['Adj Close']*trainY_after
    trainY_after=trainY_after.dropna()


    df1_test=get_data_all("data/IBM.csv",'2009-12-31','2010-12-31')
    df1_test=df1_test.reset_index()
    mac_test=MAC(df_test,12,26)
    mac_test=mac_test.dropna()
    rsi_test=RSI(df1_test,df_test,14)
    rsi_test=rsi_test.dropna()
    bv_test=bollinger_band(df_test, 20)

    bv_test=bv_test.dropna()
    dates_test=pd.date_range('2009-12-31','2010-12-31')
    df_data_test=pd.DataFrame(index=dates_test)
    df_data_test=df_data_test.join(bv_test,how='inner')
    df_data_test=df_data_test.join(mac_test,how='inner')
    df_data_test=df_data_test.join(rsi_test,how='inner')
    df_data_test=df_data_test.join(trainingY_test,how='inner')

    data_train=df_data_train.values
    data_test=df_data_test.values

    trainX = data_train[:,0:-1]
    trainY = data_train[:,-1]
    testX = data_test[:,0:-1]
    testY = data_test[:,-1]
    learner = knn.KNNLearner(6)
    learner.addEvidence(trainX,trainY)
    predictions=learner.query(trainX)

    size=len(predictions)
    one=np.ones((size,))
    predictions_change=predictions+one
    df_predictions_change=df.copy(deep=True)
    df_predictions_change=df_predictions_change[25:-5]
    i=0
    for d in df_predictions_change.index:
        df_predictions_change['Adj Close'][d]=predictions_change[i]
        i+=1
    df_predictions_price=df_predictions_change*df
    df_predictions_price=df_predictions_price.dropna()
    symbol='IBM'
    write()
    ax=df['Adj Close']['2008-02-06':].plot(title='IBM Data In Sample Entries/Exits',label='In Sample Price',color='r')
    df_predictions_price['Adj Close'].plot(label='In Sample Predicted Y',color='g',ax=ax)
    order(df_predictions_change,symbol,ax,0)
    trainY_before['Adj Close']['2008-02-06':].plot(label='In Sample Training Y',color='b',ax=ax)
    ax.legend(loc='upper left')



    rmse = math.sqrt(((trainY - predictions) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predictions, y=trainY)
    print "corr: ", c[0,1]

    predictions=learner.query(testX)
    df_test=loadDataSet("data/IBM.csv",'2009-12-31','2010-12-31')
    size=len(predictions)
    one=np.ones((size,))
    predictions_change_test=predictions+one
    df_predictions_change_test=df_test.copy(deep=True)
    df_predictions_change_test=df_predictions_change_test[25:-5]
    print df_predictions_change_test
    i=0
    for d in df_predictions_change_test.index:
        df_predictions_change_test['Adj Close'][d]=predictions_change_test[i]
        i+=1
    df_predictions_price_test=df_predictions_change_test*df_test
    df_predictions_price_test=df_predictions_price_test.dropna()


    rmse = math.sqrt(((testY - predictions) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predictions, y=testY)
    print "corr: ", c[0,1]
    plt.show()

if __name__=="__main__":
    test_run()