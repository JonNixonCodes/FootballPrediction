import pandas as pd
import numpy as np
import datetime

# Load dataframe
def load_dataframe(filename='../Data/clean_data_20200128.csv'):
    df = pd.read_csv(filename,dtype=str)
    # Convert datatypes
    NUM_COLS = ['FTAG','FTHG','AC','AF','AR','AS','AST','AY','HC','HF','HR','HS','HST','HTAG','HTHG','HY']
    DATE_COLS = ['Date']
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df[c])
    for c in DATE_COLS:
        df[c] = pd.to_datetime(df[c],dayfirst=True,errors='ignore')
    return df

# Compare home value and away value
def cmp_homeaway_val(home_val,away_val):
    ret_val = None
    if (home_val > away_val):
        ret_val = 'Home'
    elif (away_val > home_val):
        ret_val = 'Away'
    else:
        ret_val = 'Neither'
    return ret_val

# Previous matches
def prev_n_matches(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Filter date
    df = df[(df['Date']<date)]
    # Filter team
    if homeaway == 'home':
        team_mask = df['HomeTeam']==team # Home team ONLY
    elif homeaway == 'away': 
        team_mask = df['AwayTeam']==team # Away team ONLY
    else:
        team_mask = (df['HomeTeam']==team) | (df['AwayTeam']==team) # BOTH home and away
    df = df[team_mask]
    # Order by desc date
    df = df.sort_values(by='Date',ascending=False)
    # Return n results
    if n>0:
        nrows = df.shape[0]
        df=df.head(min(n,nrows)) # Return first n rows
    else:
        next # Return all
    return df

# Previous head-to-head matchups between teams
def prev_n_matchups(df,homeTeam,awayTeam,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Filter date
    df = df[(df['Date']<date)]
        # Filter team
    if homeaway == 'home':
        team_mask = (df['HomeTeam']==homeTeam) & (df['AwayTeam']==awayTeam) # home team is home ONLY
    elif homeaway == 'away': 
        team_mask = (df['HomeTeam']==awayTeam) & (df['AwayTeam']==homeTeam) # away team is away ONLY
    else:
        team_mask = (df['HomeTeam']==homeTeam) & (df['AwayTeam']==awayTeam) | (df['HomeTeam']==awayTeam) & (df['AwayTeam']==homeTeam) # include all home and away matches
    df = df[team_mask]
    # Order by desc date
    df = df.sort_values(by='Date',ascending=False)
    # Return n results
    if n>0:
        nrows = df.shape[0]
        df=df.head(min(n,nrows)) # Return first n rows
    return df

# Win or loss
def team_win_loss(teamName,homeTeam,awayTeam,FTR):
    if ((teamName==homeTeam) & (FTR=='H')) | ((teamName==awayTeam) & (FTR=='A')):
        return 'W'
    elif ((teamName==homeTeam) & (FTR=='A')) | ((teamName==awayTeam) & (FTR=='H')):
        return 'L'
    else:
        return 'D'

# Previous results
def prev_n_results(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Return results
    return list(df.apply(lambda x: team_win_loss(team,homeTeam=x['HomeTeam'],awayTeam=x['AwayTeam'],FTR=x['FTR']),axis=1))

# Number of wins in previous results
def prev_n_win(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='W' for r in results])

# Number of losses in previous results
def prev_n_loss(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='L' for r in results])

# Number of draws in previous results
def prev_n_draw(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='D' for r in results])

# Win percentage in previous results
def prev_n_win_pct(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    nwins = prev_n_win(df,team=team,n=n,date=date,homeaway=homeaway)
    return nwins/n

# Loss percentage in previous results
def prev_n_loss_pct(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    nloss = prev_n_loss(df,team=team,n=n,date=date,homeaway=homeaway)
    return nloss/n

# Goal difference from previous results
def prev_n_gd(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goal difference
    df['FTGD'] = df['FTHG']-df['FTAG']
    # Return result
    return df['FTGD'].sum()

# Average goal difference from previous results
def avg_prev_n_gd(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    return prev_n_gd(df,team=team,n=n,date=date,homeaway=homeaway)/len(prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway))

# Goals conceeded from previous results
def prev_n_gc(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goals conceeded
    df = df.apply(lambda x: x['FTAG'] if x['HomeTeam']==team else x['FTHG'], axis=1)
    # Return result
    return df.sum()

# Goals scored from previous results
def prev_n_gs(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goals scored
    df = df.apply(lambda x: x['FTHG'] if x['HomeTeam']==team else x['FTAG'], axis=1)
    # Return result
    return df.sum()

# Clean sheets from previous results
def prev_n_cs(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate clean sheets
    df = df.apply(lambda x: x['FTAG']==0 if x['HomeTeam']==team else x['FTHG']==0, axis=1)
    # Return result
    return df.sum()

# Team with most wins from previous results
def prev_n_most_wins(df,homeTeam,awayTeam,n=-1,date=datetime.datetime.today(),homeaway='both'):
    if homeaway == 'home':
        homeTeamWins = prev_n_win(df,homeTeam,n,date,'home')
        awayTeamWins = prev_n_win(df,awayTeam,n,date,'away')
    elif homeaway == 'away':
        raise Exception('User should not be looking at away results for home team')
    else:
        homeTeamWins = prev_n_win(df,homeTeam,n,date)
        awayTeamWins = prev_n_win(df,awayTeam,n,date)
    return cmp_homeaway_val(homeTeamWins,awayTeamWins)

# Team with most wins from previous head-to-head match-ups
def prev_n_matchup_wins(df,homeTeam,awayTeam,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n match-ups
    df = prev_n_matchups(df,homeTeam,awayTeam,n,date,homeaway)
    homeTeamWins = prev_n_win(df=df,team=homeTeam,date=date)
    awayTeamWins = prev_n_win(df=df,team=awayTeam,n=n,date=date)
    return cmp_homeaway_val(homeTeamWins,awayTeamWins)
