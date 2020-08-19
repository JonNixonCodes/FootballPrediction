# -*- coding: utf-8 -*-
"""
Train Naive Bayes Model

Created on Mon Jul  6 18:06:25 2020

@author: jonat
"""
# %% Load libraries
import tqdm
import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.naive_bayes import CategoricalNB
import FootballDataAnalysis as fda

# %% Load data
fd = fda.LoadFootballData()
    
# %% Assign train/validation and test splits
train_seasons = ['1718','1617','1516','1415','1314','1213','1112','1011','0910']
test_seasons = ['1819']
train_index = fd['Season'].isin(train_seasons)
test_index = fd['Season'].isin(test_seasons)

# %% Extract labels and features
X_prevResults = fda.ExtractPrevResults(fd, form='HomeAway', n=3)
X_homeTeam = fd['HomeTeam']
X_awayTeam = fd['AwayTeam']
y = fda.ExtractResult(fd, result='H')

# %% Pre-process (encoding categories)
teams = list(np.unique(X_homeTeam))
results = ['W','L','D']
labels = ['H','O']
X_prevResults = fda.EncodeCategories(X_prevResults.flatten(), 
                                     categories=results).reshape(X_prevResults.shape)
X_homeTeam = fda.EncodeCategories(X_homeTeam, categories=teams)\
    .reshape(X_homeTeam.shape)
X_awayTeam = fda.EncodeCategories(X_awayTeam, categories=teams)\
    .reshape(X_awayTeam.shape)
X = np.concatenate([X_prevResults.flatten(),X_homeTeam,X_awayTeam])\
    .reshape(X_prevResults.shape[1]+2,X_prevResults.shape[0]).transpose()
y = fda.EncodeCategories(y, categories=labels)

# %% Cross-validation (Leave-one-group-out)
X_cv, y_cv = X[train_index], y[train_index]
cv_groups = fda.EncodeCategories(fd[train_index]['Season'], train_seasons)
cv_accuracy = []
logo = LeaveOneGroupOut()
for cv_train_index, cv_test_index in tqdm.tqdm(logo.split(X_cv, y_cv, groups=cv_groups), 
                                               total=len(np.unique(cv_groups))):
    X_cvtrain, X_cvtest = X_cv[cv_train_index], X_cv[cv_test_index]
    y_cvtrain, y_cvtest = y_cv[cv_train_index], y_cv[cv_test_index]
    model = CategoricalNB().fit(X_cvtrain, y_cvtrain)
    pred = model.predict(X_cvtest)
    cv_accuracy.append(np.mean(pred==y_cvtest))

# %% Train Naive Bayes model
X_train, y_train = X[train_index], y[train_index]
X_test, y_test = X[test_index], y[test_index]
model = CategoricalNB().fit(X_train, y_train)

# %% Test Naive Bayes model
pred = model.predict(X_test)
print(f"model accuracy = {np.mean(pred==y_test)}")

# %% Analyse results
pred = pd.DataFrame(fda.DecodeCategories(pred,categories=labels),columns=['Prediction'])
y_test = pd.DataFrame(fda.DecodeCategories(y_test,categories=labels),columns=['Label'])
X_prevResults = pd.DataFrame(fda.DecodeCategories(X_test[:,[x for x in range(6)]].flatten(), categories=results).reshape(X_test.shape[0],6),columns=['H1','H2','H3','A1','A2','A3'])
X_homeTeam = pd.DataFrame(fda.DecodeCategories(X_test[:,6],categories=teams),columns=['HomeTeam'])
X_awayTeam = pd.DataFrame(fda.DecodeCategories(X_test[:,7],categories=teams),columns=['AwayTeam'])
results_df = pd.concat([X_prevResults,X_homeTeam,X_awayTeam,pred,y_test], axis='columns')
#result_df = pd.DataFrame(np.concatenate([np.transpose(X_test).flatten(),pred,y_test]).reshape(10,380).transpose())
