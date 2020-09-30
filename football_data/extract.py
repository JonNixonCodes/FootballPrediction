# -*- coding: utf-8 -*-
"""
Module: 
    football_data.extract

Description:
    This module contains functions for extracting football data from various 
    sources.
    
Created on Fri Sep 18 19:15:17 2020

@author: JonNixonCodes
"""
# %% Import libraries
import json, requests, time, tqdm, pandas as pd

# %% Define Extractor
class Extractor():
    """ 
    Extractor class for extracting football data from various sources
    
    functions:
        list_csv_sources()
        get_csv()
            
    """
    
    def __init__(self, data_config_path):
        self.config = json.load(open(data_config_path))
        self.csv_config = self.config['data_sources']['csv']
    
    def __parse_csv(self, txt, newline="\r\n", delimiter=","):
        col_names_dict = {}
        data = []
        for row_i,row in enumerate(txt.split(newline)):
            row_cells_l = row.split(delimiter)
            if row_i==0:
                col_names_dict = {c:i for i,c in enumerate(row_cells_l) if c!=""}
            elif row_cells_l[0]!="":
                row_data = {c:row_cells_l[i] 
                            for c,i in col_names_dict.items() 
                            if i<len(row_cells_l)}
                data.append(row_data)
            else:
                break
        return data    
    
    def list_csv_sources(self):
        source_list = []
        for k,v in self.csv_config.items():
            source_list.append(k)
        return print(source_list)
    
    def get_csv(self, source_name, timeout=0.1):
        data = []
        source_list = self.csv_config[source_name]['source_list']
        for source in tqdm.tqdm(source_list,total=len(source_list)):
            r = requests.get(source, allow_redirects=True)
            source_data = self.__parse_csv(r.text)
            for i in range(len(source_data)):
                source_data[i]['Source'] = source 
            data.extend(source_data)
            time.sleep(timeout)
        return pd.DataFrame(data, dtype=str)
