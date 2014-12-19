#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=============================================================================
# FileName: main.py
# Tips: 
# Author: coolws
# Date: 2014-11-08
# Email: coolws123@gmail.com
#=============================================================================
'''
from numpy import *
import SVM


print "step 1: load data..."
dataSet = []
labels = []
fileIn = open('svm.csv')
for line in fileIn.readlines():
	lineArr = line.strip().split('\t')
	dataSet.append([float(lineArr[0]), float(lineArr[1])])
	labels.append(float(lineArr[2]))

dataSet = mat(dataSet)
labels = mat(labels).T
train_x = dataSet[0:81, :]
#print "@@@@@@@@"
#print train_x
#print "@@@@@@@@"
train_y = labels[0:81, :]
test_x = dataSet[80:101, :]
test_y = labels[80:101, :]


print "training..."
C = 0.6
toler = 0.001
maxIter = 50
svmClassifier = SVM.trainSVM(train_x, train_y, C, toler, maxIter, kernelOption = ('linear', 0))


print "testing..."
accuracy = SVM.testSVM(svmClassifier, test_x, test_y)


print "show the graph..."	
print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
SVM.showSVM(svmClassifier)
