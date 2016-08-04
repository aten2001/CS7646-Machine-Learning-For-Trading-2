__author__ = 'shinshaw'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
fig = plt.figure()

inf = open('Data/KNNData.csv')
data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
X1= data[:,0]
X2=data[:,1]
Y=data[:,-1]


ax=fig.gca(projection='3d')
ax.scatter(X1,X2,Y,label='linerReg',color='DarkMagenta',linewidth=2,linestyle = '--')
rcParams['legend.fontsize'] = 11
ax.set_xlabel('X1 axis')
ax.set_ylabel('X2 axis')
ax.set_zlabel('Y axis')
plt.show()