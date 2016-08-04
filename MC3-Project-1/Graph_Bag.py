__author__ = 'shinshaw'
import math
import numpy as np
import BagLearner as bg
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
rmse_Bag_train=[]
c_Bag_train=[]
for i in range(1,60):
    learner = bg.BagLearner(learner = knn, kwargs = 3, bags = i, boost = False)
    learner.addEvidence(trainX,trainY)
    predictions=learner.query(trainX)
    rmse = math.sqrt(((trainY - predictions) ** 2).sum()/trainY.shape[0])
    c = np.corrcoef(predictions, y=trainY)
    rmse_Bag_train.append(rmse)
    c_Bag_train.append(c[0,1])
np1_train=np.array(rmse_Bag_train)
np2_train=np.array(c_Bag_train)
rmse_Bag_test=[]
c_Bag_test=[]
for i in range(1,60):
    learner = bg.BagLearner(learner = knn, kwargs = 3, bags = i, boost = False)
    learner.addEvidence(trainX,trainY)
    predictions=learner.query(testX)
    rmse = math.sqrt(((testY - predictions) ** 2).sum()/testY.shape[0])
    c = np.corrcoef(predictions, y=testY)
    rmse_Bag_test.append(rmse)
    c_Bag_test.append(c[0,1])

np1_test=np.array(rmse_Bag_test)
np2_test=np.array(c_Bag_test)
df2=pd.DataFrame(np1_test)
df1=pd.DataFrame(np1_train)
ax=df1[0].plot(title='Bagging',label='train',color='r')
df2[0].plot(label='test',ax=ax,color='g')
ax.legend(loc='upper right')
ax.set_xlabel('Bags')
ax.set_ylabel('RMSE')
plt.show()