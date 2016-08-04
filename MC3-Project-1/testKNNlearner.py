__author__ = 'shinshaw'
import math
import numpy as np
import KNNLearner as knn
if __name__=="__main__":
    inf = open('Data/ripple.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]
    learner = knn.KNNLearner(4)
    learner.addEvidence(trainX,trainY)
    predictions=learner.query(trainX)
    rmse = math.sqrt(((trainY - predictions) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predictions, y=trainY)
    print "corr: ", c[0,1]

    predictions=learner.query(testX)
    rmse = math.sqrt(((testY - predictions) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predictions, y=testY)
    print "corr: ", c[0,1]

