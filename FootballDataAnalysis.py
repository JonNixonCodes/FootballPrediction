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

def _FilterPrevResults(team, date, fg=_LoadFormGuide(), n=5, HomeAway='Both'):
    ind = (fg['Team']==team)&(fg['Datetime']<date)
    if HomeAway in ['Home','Away']:
        ind = (ind)&(fg['HomeAway']==HomeAway)
    return fg[ind].head(n).reset_index(drop=True)

# %% Extract features
def ExtractDatetime(fd):
    return pd.to_datetime(fd['Date'],dayfirst=True, errors='coerce')

def ExtractPrevResults(fd, fg=_LoadFormGuide(), n=5, form='Both'):
    """ Extract results from last N matches """
    prevResults = []
    if 'Date' not in fd.columns:
        fd['Date'] = ExtractDatetime(fd)
    for ind,row in tqdm.tqdm(fd.iterrows(),total=fd.shape[0]):
        if form == 'HomeAway':
            prevHomeTeamResults = \
                _FilterPrevResults(team=row['HomeTeam'],date=row['Date'],fg=fg,n=n,HomeAway='Home')['Result'].values
            prevAwayTeamResults = \
                _FilterPrevResults(team=row['AwayTeam'],date=row['Date'],fg=fg,n=n,HomeAway='Away')['Result'].values
        else:
            prevHomeTeamResults = \
                _FilterPrevResults(team=row['HomeTeam'],date=row['Date'],fg=fg,n=n,HomeAway='Both')['Result'].values
            prevAwayTeamResults = \
                _FilterPrevResults(team=row['AwayTeam'],date=row['Date'],fg=fg,n=n,HomeAway='Both')['Result'].values            
        prevResults.append(prevHomeTeamResults)
        prevResults.append(prevAwayTeamResults)
    return np.concatenate(prevResults).reshape(fd.shape[0],n*2)

def ExtractPrevResultsCount(fd, fg=_LoadFormGuide(), n=5, form='Both', 
                            result='W'):
    """ Extract count of previous results """
    prevResults = ExtractPrevResults(fd=fd,fg=fg,n=n,form=form)
    prevResults = (prevResults==result)
    homeTeamResultsCount = np.sum(prevResults[:,range(0,n)],axis=1)
    awayTeamResultsCount = np.sum(prevResults[:,range(n,n*2)],axis=1)
    prevResultsCount = np.concatenate([homeTeamResultsCount,awayTeamResultsCount])
    return prevResultsCount.reshape(2,fd.shape[0]).transpose()

def ExtractResult(fd, result=None):
    """ Extract full time results """
    if result==None:
        results = fd['FTR'].values
    else:
        results = fd.apply(lambda x: result if x['FTR']==result else 'O', 
                           axis='columns')
    return results
   
    
# %% User functions
def LoadFootballData(divisions=KEEP_DIVS, seasons=KEEP_SEASONS):
    fd = lfd.LoadFootballDataUK()
    fd = fd.filter(KEEP_COLS, axis='columns')
    if type(divisions)==list:
        fd = fd[fd['Div'].isin(divisions)]
    if type(seasons)==list:
        fd = fd[fd['Season'].isin(seasons)]
    return fd.reset_index(drop=True)

