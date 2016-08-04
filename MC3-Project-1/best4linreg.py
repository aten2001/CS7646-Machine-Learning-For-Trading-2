__author__ = 'shinshaw'
import numpy as np
import sys

def write():
    name='Data/linRegData.csv'
    try:
        file1 = open(name,'a')
        file1.close()
    except:
        print('Something went wrong!')
        sys.exit(0)
def dataSet(low,high,n):
	X1=np.linspace(low,high,n)
	X2=np.linspace(low,high,n)
	noise_sigma=0.05
	a=np.random.rand()
	b=np.random.rand()
	c=np.random.rand()
	Y=a*X1+b*X2+c
	noise=np.random.normal(0,noise_sigma,Y.shape)
	data=np.asarray([X1,X2,Y+noise]).T
	length=len(data)
	for i in range(length):
		f=open('Data/linRegData.csv','ab+')
		f.write(str(data[i][0])+',')
		f.write(str(data[i][1])+',')
		f.write(str(data[i][2])+'\n')

if __name__=="__main__":
	write()
	dataSet(0,1,1000)















