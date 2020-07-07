# -*- coding: utf-8 -*-
"""
Train Naive Bayes Model

Created on Mon Jul  6 18:06:25 2020

@author: jonat
"""
# %% Load libraries
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
import FootballDataAnalysis as fda

# %% Main

fd = fda.LoadFootballData()
    
# Assign train and test splits
train_seasons = ['1718','1617','1516','1415','1314','1213','1112','1011','0910']
test_seasons = ['1819']
fd_train = fd[fd['Season'].isin(train_seasons)]
fd_test = fd[fd['Season'].isin(test_seasons)]

# Extract labels and features
X_train = fda.ExtractPrevResults(fd_train)
X_test = fda.ExtractPrevResults(fd_test)
y_train = fda.ExtractResult(fd_train)
y_test = fda.ExtractResult(fd_test)

# Pre-process (encoding categories)
X_le = preprocessing.LabelEncoder()
X_le.fit(['W','L','D'])
X_train = X_le.transform(X_train.flatten()).reshape(X_train.shape)
X_test = X_le.transform(X_test.flatten()).reshape(X_test.shape)
y_le = preprocessing.LabelEncoder()
y_le.fit(['H','A','D'])
y_train = y_le.transform(y_train)
y_test = y_le.transform(y_test)

# Train Naive Bayes Model
model = MultinomialNB().fit(X_train, y_train)

# Test Naive Bayes Model
predicted = model.predict(X_test)
print(f"model accuracy = {np.mean(predicted == y_test)}")
