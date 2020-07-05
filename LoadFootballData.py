# -*- coding: utf-8 -*-
"""
Load Football Data

Created on Sat Jun 20 19:13:44 2020

@author: jonat
"""
# %% Load Libraries
import re, requests
import pandas as pd
from bs4 import BeautifulSoup

# %% Constants
MAIN_URL = "http://www.football-data.co.uk/englandm.php"
URL_REGEX = re.compile(r"mmz4281.*\.csv")
OUTPUT_DIR = "./Data/FootballDataUK/"
INPUT_FILEPATH = "./Data/FootballDataUK/Consolidated/FootballDataUK_93_20.csv"

# %% Helper Functions
def ExtractFileUrl(elem):
    url = None
    elem = elem.attrs['href']
    file_match_object = re.compile(r"mmz4281.*\.csv").search(elem)
    if file_match_object != None:
        url = "http://www.football-data.co.uk/"+file_match_object.string
    return url

def FilterSoup(soup):
    anchor_elements = soup.findAll('a')
    urls = list(map(ExtractFileUrl,anchor_elements))
    urls = [url for url in urls if url!=None] 
    return urls

#FilterUrl = lambda x: URL_REGEX.search(x) != None
#PrependUrl = lambda x: "http://www.football-data.co.uk/"+x
#GetUrl = lambda x: x.attrs['href']
#GetFileName = lambda x: "_".join(re.split(r"[/.]",x)[-3:-1])+".csv"

# %% User Functions
def DownloadFootballDataUK(output_dir=OUTPUT_DIR):
    response = requests.get(MAIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    anchor_elements = soup.findAll('a')
    file_urls = FilterSoup(soup)
    for ind,url in enumerate(file_urls):
        r = requests.get(url, allow_redirects=True)
        fname = output_dir+"_".join(re.split(r"[/.]",url)[-3:-1])+".csv"
        print(f"\tSaving file {ind+1}/{len(file_urls)}",end='\r', flush=True)
        with open(fname, 'wb') as f:
            f.write(r.content)
    print("\tFinished",end="\n", flush=False)
    return None

def LoadFootballDataUK(filepath=INPUT_FILEPATH):
    return pd.read_csv(filepath, sep="\t", dtype=str)

# %% Main
def main():
    print("Main function not implemented")
    return None

if __name__=="main":
    main()