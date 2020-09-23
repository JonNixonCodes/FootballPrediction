# -*- coding: utf-8 -*-
"""
Module: 
    football_data.ingest

Description:
    This module contains functions for transforming and loading football data 
    from various sources into a MongoEngine database.
    
Created on Tue Sep 22 21:31:44 2020

@author: JonNixonCodes
"""
# %% Import libraries
import json, requests, time, tqdm, pandas as pd
from mongoengine import *
from football_data.extract import Extractor

# %% Define documents
class Match(Document):
    home_team = StringField(required=True)
    away_team = StringField(required=True)
    date = DateField(required=True)
    competition = StringField()
    season = StringField()
    round = StringField()
    stadium = StringField()
    FTR = StringField()

# %% Define ingestor
class Ingestor:
    """ 
    Ingestor class for transforming football and loading data from various 
    sources        
    """
    def __init__(self, data_config_path):
        self.config = json.load(open(data_config_path))
        self.csv_config = self.config['data_sources']['csv']
        self.extractor = Extractor(data_config_path)
        connect('football-data')
        
    def ingest_match(self, source_name):
        if source_name=="football_data_uk_current":
            next
        else:
            return
        match_df = self.extractor.get_csv(source_name)
        for ind,row in tqdm.tqdm(match_df.iterrows(), total=match_df.shape[0]):
            match = Match()
            match.home_team = row["HomeTeam"]
            match.away_team = row["AwayTeam"]
            match.date = row["Date"]
            match.FTR = row["FTR"]
            match.save()
    
    