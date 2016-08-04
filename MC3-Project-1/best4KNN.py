__author__ = 'shinshaw'
import numpy as np
import sys

def write():
    name='Data/KNNData2.csv'
    try:
        file1 = open(name,'a')
        file1.close()
    except:
        print('Something went wrong!')
        sys.exit(0)
def dataSet(n):
    X1=np.random.randint(1,100,size=n)
    X2=np.random.randint(1,100,size=n)
    Y=np.zeros((n,))


    for i in range(n):
        if X1[i]>X2[i]:
            Y[i]=1
        elif X1[i]<X2[i]:
            Y[i]=-1
        else:
            Y[i]=0

    data=np.asarray([X1,X2,Y]).T
    length=len(data)
    for i in range(length):
		f=open('Data/KNNData2.csv','ab+')
		f.write(str(data[i][0])+',')
		f.write(str(data[i][1])+',')
		f.write(str(data[i][2])+'\n')

if __name__=="__main__":
	write()
	dataSet(1000)



