# -*- coding: utf-8 -*-
"""
Module: 
    football_data.schema

Description:
    This module contains schema definitions for football_data database

Created on Tue Sep 29 22:57:47 2020

@author: JonNixonCodes
"""
# %% Import libraries
from mongoengine import *

# %% Define schema
class Match(Document):
    home_team = StringField(required=True)
    away_team = StringField(required=True)
    date = DateField(required=True, unique_with=['home_team','away_team'])
    date_time = DateTimeField()
    competition = StringField()
    season = StringField()
    round = StringField()
    stadium = StringField()
    referee = StringField()
    FTR = StringField()
    HTR = StringField()
    FTHG = IntField()
    FTAG = IntField()
    HTHG = IntField()
    HTAG = IntField()
    HS = IntField()
    AS = IntField()
    HST = IntField()
    AST = IntField()
    HF = IntField()
    AF = IntField()
    HC = IntField()
    AC = IntField()
    HY = IntField()
    AY = IntField()
    HR = IntField()
    AR = IntField()
    last_updated = DateTimeField(required=True)

