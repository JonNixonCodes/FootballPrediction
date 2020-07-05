# -*- coding: utf-8 -*-
"""
Football Analysis Functions

Created on Wed Jul  1 21:32:44 2020

@author: jonat
"""
# %% Load libraries
import tqdm
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
import LoadFootballData as lfd

# %% Constants
KEEP_COLS = ['Div',
             'Season',
             'Date',
             'HomeTeam',
             'AwayTeam',
             'FTHG',
             'FTAG',
             'FTR',
             'HTHG',
             'HTAG',
             'HTR',
             'Attendance',
             'Referee',
             'HS',
             'AS',
             'HST',
             'AST',
             'HHW',
             'AHW',
             'HC',
             'AC',
             'HF',
             'AF',
             'HO',
             'AO',
             'HY',
             'AY',
             'HR',
             'AR']

KEEP_SEASONS = ['1819',
                '1718',
                '1617',
                '1516',
                '1415',
                '1314',
                '1213',
                '1112',
                '1011',
                '0910']

KEEP_DIVS = ['E0']

# %% Helper functions
def _WinLossDraw(HomeAway,FTR):
    result = None
    if HomeAway=='Home':
        if FTR=='H':
            result = 'W'
        elif FTR=='A':
            result = 'L'
        else:
            result = 'D'
    elif HomeAway=='Away':
        if FTR=='H':
            result = 'L'
        elif FTR=='A':
            result = 'W'
        else:
            result = 'D'
    return result

def _LoadFormGuide():
    """Returns all match results indexed by Team and Date"""
    fd = lfd.LoadFootballDataUK()
    fd_h = fd.copy()
    fd_h['Team'] = fd_h['HomeTeam']
    fd_h['HomeAway'] = 'Home'
    fd_h['Result'] = fd_h\
        .apply(lambda x: _WinLossDraw(x['HomeAway'],x['FTR']), axis='columns')
    fd_a = fd.copy()
    fd_a['Team'] = fd_a['AwayTeam']
    fd_a['HomeAway'] = 'Away'
    fd_a['Result'] = fd_a\
        .apply(lambda x: _WinLossDraw(x['HomeAway'],x['FTR']), axis='columns')
    fg = pd.concat([fd_h,fd_a], axis='index')
    fg = fg.filter(['Team','Date','HomeAway','Result'])
    fg['Datetime'] = pd.to_datetime(fg['Date'],dayfirst=True, errors='coerce')
    fg = fg.sort_values(by='Datetime', ascending=False, ignore_index=True, axis='index')
    return fg

def _FilterPrevResults(team, date, fg=_LoadFormGuide(), n=5):
    ind = (fg['Team']==team)&(fg['Datetime']<date)
    return fg[ind].head(n).reset_index(drop=True)

# %% Extract features
def ExtractDatetime(fd):
    return pd.to_datetime(fd['Date'],dayfirst=True, errors='coerce')

def ExtractPrevResults(fd, fg=_LoadFormGuide(), n=5):
    """Returns matrix of last N matches"""
    prevResults = []
    #colNames = [f"HLR{i}" for i in range(n)] + [f"ALR{i}" for i in range(n)]
    if 'Date' not in fd.columns:
        fd['Date'] = ExtractDatetime(fd)
    for ind,row in tqdm.tqdm(fd.iterrows(),total=fd.shape[0]):
        prevHomeTeamResults = \
            _FilterPrevResults(team=row['HomeTeam'],date=row['Date'],fg=fg,n=n)['Result'].values
        prevAwayTeamResults = \
            _FilterPrevResults(team=row['AwayTeam'],date=row['Date'],fg=fg,n=n)['Result'].values
        prevResults.append(prevHomeTeamResults)
        prevResults.append(prevAwayTeamResults)
    #return pd.DataFrame(data=np.concatenate(prevResults).reshape(fd.shape[0],n*2),columns=colNames)
    return np.concatenate(prevResults).reshape(fd.shape[0],n*2)

def ExtractFTR(fd):
    """Returns array of full time results"""
    return fd['FTR'].values

def ExtractHomeWins(fd):
    """Returns array of home wins (H) vs other result (O)"""
    fd.apply(lambda x: 'W' if x['FTR']=='')
    
# %% User functions
def LoadFootballData(divisions=KEEP_DIVS, seasons=KEEP_SEASONS):
    fd = lfd.LoadFootballDataUK()
    fd = fd.filter(KEEP_COLS, axis='columns')
    if type(divisions)==list:
        fd = fd[fd['Div'].isin(divisions)]
    if type(seasons)==list:
        fd = fd[fd['Season'].isin(seasons)]
    return fd.reset_index(drop=True)

# %% Main
fd = LoadFootballData()
    
# Assign train and test splits
train_seasons = ['1718','1617','1516','1415','1314','1213','1112','1011','0910']
test_seasons = ['1819']
fd_train = fd[fd['Season'].isin(train_seasons)]
fd_test = fd[fd['Season'].isin(test_seasons)]

# Extract labels and features
X_train = ExtractPrevResults(fd_train)
X_test = ExtractPrevResults(fd_test)
y_train = ExtractFTR(fd_train)
y_test = ExtractFTR(fd_test)

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
