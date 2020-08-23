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
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.naive_bayes import CategoricalNB

# %% Load features
features_filename = "features.csv"
features = pd.read_csv(f"Features/{features_filename}",sep="\t",dtype=str)
    
# %% Assign train/validation and test splits
train_seasons = ['1718','1617','1516','1415','1314','1213','1112','1011','0910']
test_seasons = ['1819']
train_index = features['Season'].isin(train_seasons)
test_index = features['Season'].isin(test_seasons)

# %% Define features and labels
label = features.apply(lambda x: 'H' if x['FTR']=='H' else 'O', axis='columns')
features = features.drop(['FTR'], axis='columns')

# %% Pre-process (encoding categories)
encoder = preprocessing.OrdinalEncoder()
label_encoder = preprocessing.LabelEncoder()
encoded_features = encoder.fit_transform(features)
label = label_encoder.fit_transform(label)

# %% Assign features, labels, cv groups
seasons = encoded_features[:,-1]
X = encoded_features[:,:-1]
y = label

# %% Cross-validation (Leave-one-group-out)
X, y, cv_groups = X[train_index], y[train_index], seasons[train_index]
cv_accuracy = []
logo = LeaveOneGroupOut()
for cv_train_index, cv_test_index in logo.split(X, y, groups=cv_groups):
    X_train, X_test = X[cv_train_index], X[cv_test_index]
    y_train, y_test= y[cv_train_index], y[cv_test_index]
    model = CategoricalNB().fit(X_train, y_train)
    pred = model.predict(X_test)
    cv_accuracy.append(np.mean(pred==y_test))
print(f"cross-validation accuracy = {np.mean(cv_accuracy)}")

# %% Assign features, labels, cv groups
seasons = encoded_features[:,-1]
y = label
X = encoded_features[:,:-1]

# %% Train Naive Bayes model
X_train, y_train = X[train_index], y[train_index]
X_test, y_test = X[test_index], y[test_index]
model = CategoricalNB().fit(X_train, y_train)

# %% Test Naive Bayes model
pred = model.predict(X_test)
print(f"model accuracy = {np.mean(pred==y_test)}")

# %% Analyse results
results = features[test_index].reset_index(drop=True)
results.loc[:,'label'] = pd.Series(label_encoder.inverse_transform(label[test_index]))
results.loc[:,'prediction'] = pd.Series(label_encoder.inverse_transform(pred))
