#coding:utf-8

# Numpy: http://sourceforge.net/projects/numpy/files/NumPy/1.8.1/
# Scipy: http://sourceforge.net/projects/scipy/files/scipy/0.14.0/
# matplotlib: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.1/
import math
import numpy as np
import pylab as pl
import random 

def distance(a, b):
    return (a[0]- b[0]) ** 2 + (a[1] - b[1]) ** 2

def k_means(x, y, k_count):
    
    count = len(x)
    
    #确定每一维的上、下界
    ranges=[(min(x),max(x)),(min(y),max(y))]
    #print ranges

    
    #随机放置K个点
    k_point=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
    for i in range(len(ranges[0]))] for j in range(k_count)]
    k_point.sort()
    
    
    while True:
        km = [[] for i in range(k_count)]      #存储每个集合的索引
        #遍历所有点
        for i in range(count):
            cp = [x[i], y[i]]                   #当前点
            #计算点到各个集合中心点的距离
            distances = [distance(k_point[j], cp) for j in range(k_count)]
            min_index = distances.index(min(distances))   
            #把将点加入某集合
            km[min_index].append(i)

        #更换集合中心
        k_new = []
        for i in range(k_count):
            _x = sum([x[j] for j in km[i]]) / len(km[i])
            _y = sum([y[j] for j in km[i]]) / len(km[i])
            k_new.append([_x, _y])

        k_new.sort()       
        if (k_new != k_point):
            k_point = k_new
        else:
            return km

x, y = np.loadtxt('k_means.csv', delimiter=',', unpack=True)
k_count = 3
km = k_means(x, y, k_count)


#Matplotlab画图
pl.plot([x[i] for i in km[0]], [y[i] for i in km[0]], 'or')
pl.plot([x[i] for i in km[1]], [y[i] for i in km[1]], 'og')
pl.plot([x[i] for i in km[2]], [y[i] for i in km[2]], 'ob')

pl.show()
