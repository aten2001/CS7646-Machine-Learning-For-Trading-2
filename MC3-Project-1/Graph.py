__author__ = 'shinshaw'
import math
import numpy as np
import KNNLearner as knn
import matplotlib.pyplot as plt
import pandas as pd

inf = open('Data/ripple.csv')
data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
train_rows = math.floor(0.6* data.shape[0])
test_rows = data.shape[0] - train_rows
trainX = data[:train_rows,0:-1]
trainY = data[:train_rows,-1]
testX = data[train_rows:,0:-1]
testY = data[train_rows:,-1]
rmse_KNN_train=[]
c_KNN_train=[]
for i in range(1,21):
    learner = knn.KNNLearner(i)
    learner.addEvidence(trainX,trainY)
    predictions_train=learner.query(trainX)
    rmse_train = math.sqrt(((trainY - predictions_train) ** 2).sum()/trainY.shape[0])
    c_train = np.corrcoef(predictions_train, y=trainY)
    rmse_KNN_train.append(rmse_train)
    c_KNN_train.append(c_train[0,1])
np1_train=np.array(rmse_KNN_train)
np2_train=np2_test=np.array(c_KNN_train)

rmse_KNN_test=[]
c_KNN_test=[]
for i in range(1,21):
    learner = knn.KNNLearner(i)
    learner.addEvidence(trainX,trainY)
    predictions_test=learner.query(testX)
    rmse = math.sqrt(((testY - predictions_test) ** 2).sum()/testY.shape[0])
    c = np.corrcoef(predictions_test, y=testY)
    rmse_KNN_test.append(rmse)
    c_KNN_test.append(c[0,1])
np1_test=np.array(rmse_KNN_test)

np2_test=np.array(c_KNN_test)
df2=pd.DataFrame(np1_test)
df1=pd.DataFrame(np1_train)
df1[0]=df1[0][1:]

ax=df1[0].plot(title='KNN',label='train',color='r')
df2[0]=df2[0][1:]
df2[0].plot(label='test',ax=ax,color='g')
ax.legend(loc='upper right')
ax.set_xlabel('k')
ax.set_ylabel('RMSE')
plt.show()
