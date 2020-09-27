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
import json, tqdm, datetime, pandas as pd
from mongoengine import *
from football_data.extract import Extractor

# %% Declare constants
_MATCH_SOURCES = ["football_data_uk_current","football_data_uk_full"]

# %% Define documents
class Match(Document):
    home_team = StringField(required=True)
    away_team = StringField(required=True)
    date = DateField(required=True, unique_with=['home_team','away_team'])
    competition = StringField()
    season = StringField()
    round = StringField()
    stadium = StringField()
    FTR = StringField()
    last_updated = DateTimeField(required=True)

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
    
    def __get_match(self,home_team,away_team,date):
        match = Match.objects(home_team=home_team,away_team=away_team,date=date).first()
        if match == None:
            match = Match(home_team=home_team,away_team=away_team,date=date)
        match.last_updated = datetime.datetime.today()
        return match
            
    
    def ingest_match(self, source_name):
        if source_name in _MATCH_SOURCES:
            next
        else:
            return
        match_df = self.extractor.get_csv(source_name)
        for ind,row in tqdm.tqdm(match_df.iterrows(), total=match_df.shape[0]):
            match = self.__get_match(home_team=row["HomeTeam"],
                                     away_team=row["AwayTeam"],
                                     date=row["Date"])
            match.FTR = row["FTR"]
            match.save()
    
    