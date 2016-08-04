__author__ = 'shinshaw'
import numpy as np
import random
import KNNLearner as knn

class BagLearner(object):
    def __init__(self,learner,kwargs,bags,boost):
        self.learner= knn.KNNLearner
        self.bags=bags
        self.boost=False
        self.kwargs= {"k":3}

    def addEvidence(self,trainX,trainY):
        length=len(trainX)
        d=trainX[0].size+trainY[0].size
        trainSet=np.empty((length,d))
        for i in range(length):
            trainSet[i][0]=trainX[i][0]
            trainSet[i][1]=trainX[i][1]
            trainSet[i][2]=trainY[i]
        self.trainX=trainX
        self.trainY=trainY
        self.trainSet=trainSet

    def query(self,testX):
        trainX=self.trainX
        trainY=self.trainY
        trainSet=self.trainSet
        num=len(trainX)
        length=len(testX)
        bags=self.bags
        predictions=np.zeros((length,),dtype=float)
        for i in range(bags):
            samplelist=[]
            for j in range(num):
                X=random.sample(trainSet, 1)
                samplelist.append(X[0])
            sample=np.array(samplelist)
            sampleX = sample[:num,0:-1]
            sampleY = sample[:num,-1]
            learner = self.learner(self.kwargs["k"])
            learner.addEvidence(sampleX,sampleY)
            prediction=learner.query(testX)
            prediction_array=np.array(prediction)

            predictions=predictions+prediction_array
        result=predictions/bags
        return result



