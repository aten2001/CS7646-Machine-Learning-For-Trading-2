
__author__ = 'shinshaw'
import numpy as np
import math
import operator

class KNNLearner(object):
    def __init__(self,K):
        self.K=K

    def addEvidence(self,trainX,trainY):
        self.trainX=trainX
        self.trainY=trainY


    def query(self,testX):
        trainX=self.trainX
        trainY=self.trainY
        def euclideanDistance(dataX1,dataX2,length):
            distance=0
            for x in range(length):
                distance+=pow((dataX1[x]-dataX2[x]),2)
            return math.sqrt(distance)
        def getNeighbors(trainX,trainY,testData, k):
	        distances = []
	        length = len(testData)
	        for x in range(len(trainX)):
		        dist = euclideanDistance(testData, trainX[x], length)
		        distances.append((trainY[x], dist))
	        distances.sort(key=operator.itemgetter(1))
	        neighbors = []
	        for x in range(k):
		        neighbors.append(distances[x][0])
	        return neighbors
        def getPrediction(neighbors):
	        pred=0
	        for x in range(len(neighbors)):
		        pred = pred+neighbors[x]
	        pred=pred/self.K
	        return pred
        k=3
        predictions=[]
        for x in range(len(testX)):
            neighbors=getNeighbors(trainX,trainY,testX[x],self.K)
            result=getPrediction(neighbors)
            predictions.append(result)
        return predictions





