# -*- coding: utf-8 -*-
"""
Train Naive Bayes Model

Created on Mon Jul  6 18:06:25 2020

@author: jonat
"""
# %% Load libraries
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import FootballDataAnalysis as fda

# %% Load data
fd = fda.LoadFootballData()
    
# %% Assign train and test splits
train_seasons = ['1718','1617','1516','1415','1314','1213','1112','1011','0910']
test_seasons = ['1819']
fd_train = fd[fd['Season'].isin(train_seasons)]
fd_test = fd[fd['Season'].isin(test_seasons)]

# %% Extract labels and features
X_train = fda.ExtractPrevResults(fd_train, form='HomeAway', n=3)
X_test = fda.ExtractPrevResults(fd_test, form='HomeAway', n=3)
y_train = fda.ExtractResult(fd_train, result='H')
y_test = fda.ExtractResult(fd_test, result='H')

# %% Pre-process (encoding categories)
X_train_enc = fda.EncodeCategories(X_train.flatten(), categories=['W','L','D']).reshape(X_train.shape)
X_test_enc = fda.EncodeCategories(X_test.flatten(), categories=['W','L','D']).reshape(X_test.shape)
y_train_enc = fda.EncodeCategories(y_train, categories=['H','O'])
y_test_enc = fda.EncodeCategories(y_test, categories=['H','O'])


# %% Train Naive Bayes Model
model = MultinomialNB().fit(X_train_enc, y_train_enc)

# %% Test Naive Bayes Model
predicted = model.predict(X_test_enc)
print(f"model accuracy = {np.mean(predicted == y_test_enc)}")

# %% Analyse results
predicted = fda.DecodeCategories(predicted, categories=['H','O'])
result_df = pd.DataFrame(np.concatenate([np.transpose(X_test).flatten(),predicted,y_test]).reshape(8,380).transpose())
