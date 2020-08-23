# -*- coding: utf-8 -*-
"""
Extract features from football data

Created on Mon Jul  6 18:06:25 2020

@author: jonat
"""
# %% Load libraries
import pandas as pd
import numpy as np
import FootballDataAnalysis as fda

# %% Load data
fd = fda.LoadFootballData()

# %% Extract labels and features
prevResults = pd.DataFrame(fda.ExtractPrevResults(fd, form='HomeAway', n=3), 
                              columns=['H1','H2','H3','A1','A2','A3'])
homeTeam = fd['HomeTeam']
awayTeam = fd['AwayTeam']
season = fd['Season']
label = fd['FTR']
features_df = pd.concat([prevResults,
                         homeTeam,
                         awayTeam,
                         season,
                         label], axis='columns')

# %% Export features
features_filename = "features.csv"
features_df.to_csv(f"Features/{features_filename}",sep="\t",index=False)
