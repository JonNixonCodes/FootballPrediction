# Import Libraries
import pandas as pd
import numpy as np
import datetime
import FootballDB as fdb

# Define Constants
FILTER_SEASONS = ['0001','0102','0203','0304','0405','0506','0607','0708','0809','0910','1011','1112','1213','1314','1415','1516','1617','1718','1819']
FILTER_DIV = ['E0','E1']
NUM_COLS = ['FTAG','FTHG','AC','AF','AR','AS','AST','AY','HC','HF','HR','HS','HST','HTAG','HTHG','HY']
## Valid for feature table
VALID_SEASONS = ['1617','1718','1819']
VALID_DIV = ['E0']
BASE_COLS = ['HomeTeam','AwayTeam','Date','Season','Div','FTR']
    
# Feature Engineering
## Previous matches
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
        df=df.iloc[range(n)] # Return first n rows
    else:
        next # Return all
    return df

## Win or loss
def team_win_loss(teamName,homeTeam,awayTeam,FTR):
    if ((teamName==homeTeam) & (FTR=='H')) | ((teamName==awayTeam) & (FTR=='A')):
        return 'W'
    elif ((teamName==homeTeam) & (FTR=='A')) | ((teamName==awayTeam) & (FTR=='H')):
        return 'L'
    else:
        return 'D'

## Previous results
def prev_n_results(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Return results
    return list(df.apply(lambda x: team_win_loss(team,homeTeam=x['HomeTeam'],awayTeam=x['AwayTeam'],FTR=x['FTR']),axis=1))

## Number of wins in previous results
def prev_n_win(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='W' for r in results])

## Number of losses in previous results
def prev_n_loss(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='L' for r in results])

## Number of draws in previous results
def prev_n_draw(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    results = prev_n_results(df,team=team,n=n,date=date,homeaway=homeaway)
    return sum([r=='D' for r in results])

## Win percentage in previous results
def prev_n_win_pct(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    nwins = prev_n_win(df,team=team,n=n,date=date,homeaway=homeaway)
    return nwins/n

## Loss percentage in previous results
def prev_n_loss_pct(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    nloss = prev_n_loss(df,team=team,n=n,date=date,homeaway=homeaway)
    return nloss/n

## Goal difference from previous results
def prev_n_gd(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goal difference
    df['FTGD'] = df['FTHG']-df['FTAG']
    # Return result
    return df['FTGD'].sum()

## Average goal difference from previous results
def avg_prev_n_gd(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    return prev_n_gd(df,team=team,n=n,date=date,homeaway=homeaway)/len(prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway))

## Goals conceeded from previous results
def prev_n_gc(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goals conceeded
    df = df.apply(lambda x: x['FTAG'] if x['HomeTeam']==team else x['FTHG'], axis=1)
    # Return result
    return df.sum()

## Goals scored from previous results
def prev_n_gs(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate goals scored
    df = df.apply(lambda x: x['FTHG'] if x['HomeTeam']==team else x['FTAG'], axis=1)
    # Return result
    return df.sum()

## Clean sheets from previous results
def prev_n_cs(df,team,n=-1,date=datetime.datetime.today(),homeaway='both'):
    # Get previous n matches
    df = prev_n_matches(df,team=team,n=n,date=date,homeaway=homeaway)
    # Calculate clean sheets
    df = df.apply(lambda x: x['FTAG']==0 if x['HomeTeam']==team else x['FTHG']==0, axis=1)
    # Return result
    return df.sum()

# Main
def main():
    # Load dataframe
    db = fdb.LoadDB()
    fduk = fdb.LoadTbl(db,'football-data-uk')
    df = fdb.LoadDframe(fduk)
    # Convert datatypes
    df['Date'] = pd.to_datetime(df['Date'],dayfirst=True,errors='ignore')
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df[c])
    # Filter dataframe
    df = df[df['Season'].isin(FILTER_SEASONS)]
    df = df[df['Div'].isin(FILTER_DIV)]
    # Impute missing data with mean values
    ## Missing data
    missing_df = df[df.isna().max(axis=1)] 
    ## Calculate impute values
    impute_vals = df.groupby(['Div','FTR','Season']).mean().reset_index()
    impute_vals['HTR']=impute_vals['FTR']
    impute_vals['Referee']='Unknown'
    ## Impute dataframe
    df.loc[missing_df.index]=df.loc[missing_df.index].apply(lambda x: x.fillna(impute_vals[(impute_vals['Div']==x['Div']) & (impute_vals['FTR']==x['FTR']) & (impute_vals['Season']==x['Season'])].iloc[0]),axis=1)
    # Create feature table
    feature_df = df[(df['Season'].isin(VALID_SEASONS)) & (df['Div'].isin(VALID_DIV))]
    feature_df = feature_df.filter(BASE_COLS)
    # Add feature variables
    feature_df['home_prev_3_result'] = feature_df.apply(lambda x: "".join(prev_n_results(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both')),axis=1)
    feature_df['home_prev_3_win'] = feature_df.apply(lambda x: prev_n_win(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_loss'] = feature_df.apply(lambda x: prev_n_loss(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_draw'] = feature_df.apply(lambda x: prev_n_draw(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_win_pct'] = feature_df.apply(lambda x: prev_n_win_pct(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_loss_pct'] = feature_df.apply(lambda x: prev_n_loss_pct(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_gd'] = feature_df.apply(lambda x: prev_n_gd(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_gc'] = feature_df.apply(lambda x: prev_n_gc(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_gs'] = feature_df.apply(lambda x: prev_n_gs(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['home_prev_3_cs'] = feature_df.apply(lambda x: prev_n_cs(df,team=x['HomeTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_result'] = feature_df.apply(lambda x: "".join(prev_n_results(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both')),axis=1)
    feature_df['away_prev_3_win'] = feature_df.apply(lambda x: prev_n_win(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_loss'] = feature_df.apply(lambda x: prev_n_loss(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_draw'] = feature_df.apply(lambda x: prev_n_draw(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_win_pct'] = feature_df.apply(lambda x: prev_n_win_pct(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_loss_pct'] = feature_df.apply(lambda x: prev_n_loss_pct(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_gd'] = feature_df.apply(lambda x: prev_n_gd(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_gc'] = feature_df.apply(lambda x: prev_n_gc(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_gs'] = feature_df.apply(lambda x: prev_n_gs(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    feature_df['away_prev_3_cs'] = feature_df.apply(lambda x: prev_n_cs(df,team=x['AwayTeam'],n=3,date=x['Date'],homeaway='both'),axis=1)
    # Setup feature table in database
    feature_tbl = fdb.SetupTbl(db,"features")
    # Export feature table
    ## Convert date column to string
    feature_df['Date'] = feature_df.apply(lambda x: x['Date'].strftime("%Y-%m-%d"), axis=1)
    fdb.ImportDframe(dframe=feature_df,dbase=db)

if __name__ == "__main__":
    main()
    
