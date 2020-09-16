# -*- coding: utf-8 -*-
"""
Module: 
    football_data.mining

Description:
    This module contains functions for mining football data from various 
    sources.

Created on Wed Sep 16 21:04:13 2020

@author: JonNixonCodes
"""

# %% Import Libraries
import re, requests, tqdm
from bs4 import BeautifulSoup

# %% Define Constants
FDUK_URL = "http://www.football-data.co.uk/englandm.php"
FDUK_REGEX = re.compile(r"mmz4281.*\.csv")

# %% Helper Functions
_filter_url = lambda x: FDUK_REGEX.search(x) != None
_prepend_url = lambda x: "http://www.football-data.co.uk/"+x
_get_url = lambda x: x.attrs['href']
_get_filename = lambda x: "_".join(re.split(r"[/.]",x)[-3:-1])+".csv"

# %% User Functions
def download_football_data_uk(landing_dir):
    response = requests.get(FDUK_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    anchor_tags = soup.findAll('a')
    urls_l = list(map(_get_url, anchor_tags))
    urls_l = list(filter(_filter_url, urls_l))
    urls_l = list(map(_prepend_url, urls_l))
    for url in tqdm.tqdm(urls_l,total=len(urls_l)):
        r = requests.get(url, allow_redirects=True)
        fname = _get_filename(url)
        fpath = landing_dir+fname
        with open(fpath, 'wb') as f:
            f.write(r.content)

def download_fixture_download(landing_dir
                              ,competitions=['epl','championship']
                              ,seasons=['2016','2017','2018','2019','2020']):
    for c in competitions:
        for s in seasons:
            url = f"https://fixturedownload.com/download/{c}-{s}-GMTStandardTime.csv"
            r = requests.get(url, allow_redirects=True)
            if r.status_code==200:
                fpath = landing_dir+re.split(r"[/]",url)[-1]
                with open(fpath, 'wb') as f:
                    f.write(r.content)                
            
    
