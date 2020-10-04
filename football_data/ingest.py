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
import json, tqdm, datetime, re, pandas as pd, numpy as np
from mongoengine import *
from football_data.extract import Extractor
from football_data.schema import Match

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
    
    def __convert_data_type(self,value,dtype):
        ret_value = value
        if dtype=="int":
            ret_value = int(value)
        elif dtype=="date":
            if len(value)==10:
                ret_value = datetime.datetime.strptime(value,"%d/%m/%Y")
            elif len(value)==8:
                ret_value = datetime.datetime.strptime(value,"%d/%m/%y")
        return ret_value
        
        
    def __read_row_data(self,row,data_dict):
        data = {}
        for k,v in data_dict.items():
            col_name, schema_name, dtype = k,v['name'],v['type']
            if (col_name in row) and (row[col_name] not in [np.nan,None,""]):
                try:
                    data[schema_name]=self.__convert_data_type(row[col_name],dtype)
                except:
                    pass
        return data
    
    def __format_date_time(self,date,time):
        date_time = None
        try:
            date_str = datetime.datetime.strftime(date,"%d/%m/%Y")
            time_str = "00:00" if time==np.nan else time
            date_time_str = date_str+" "+time_str            
            date_time = datetime.datetime.strptime(date_time_str,"%d/%m/%Y %H:%M")
        except:
            pass
        return date_time
    
    def __parse_season(self, source):
        season = None
        pattern = re.compile("/\d{4}/")
        tmp_l = pattern.findall(source)
        if len(tmp_l)>0:
            season = tmp_l[0].strip("/")
        return season
    
    def ingest_match(self,source_name,extract_df):
        data_dict = self.csv_config[source_name]['data_dict']
        for ind,row in tqdm.tqdm(extract_df.iterrows(), total=extract_df.shape[0]):
            match_data = self.__read_row_data(row,data_dict)
            match = self.__get_match(home_team=match_data['home_team'],
                                     away_team=match_data['away_team'],
                                     date=match_data['date'])
            for k,v in match_data.items():
                if k not in ['div','time','source']:
                    match[k] = v
            if 'date' in match_data and 'time' in match_data:
                match['date_time'] = self.__format_date_time(match_data['date'],match_data['time'])
            if 'div' in match_data:
                match['competition'] = match_data['div']
            if 'source' in match_data:
                match['season'] = self.__parse_season(match_data['source'])
            match.save()
    
    