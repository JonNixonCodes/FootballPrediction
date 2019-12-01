import glob
import pandas as pd
import json
from tinydb import TinyDB, Query
import FootballDB as fdb

# Load list of columns to keep from file
def load_keep_columns(fname):
    with open(fname) as f:
        colMap = json.load(f)
    keepCols = [k for k,v in colMap.items() if v==1]
    return keepCols

def strip_filename_season(fname):
    tmp = fname.split('/')[-1]
    return tmp.split('_')[0]

# Fix: remove trailing commas from csv
def strip_trail_commas(in_file):
    lines = []
    with open(in_file,'r',encoding='cp1252') as f:
        for ln in f:
            ln = ln.rstrip("\n")
            ln = ln.rstrip(',')
            ln = ln.split(',')
            lines.append(ln)
    col_names = lines[0]
    col_vals = lines[1:]
    return pd.DataFrame(col_vals,columns=col_names)

# Join data from list of files into a dataframe    
def join_files(flist):
    df = pd.DataFrame()
    for f in flist:
        try:
            df = df.append(pd.read_csv(f,encoding='cp1252'),ignore_index=True)
        except pd.errors.ParserError:
            df = df.append(strip_trail_commas(f),ignore_index=True)
    return df

# Convert csv file into a dataframe
def csv_to_dataframe(fname):
    try:
        df = pd.read_csv(fname,encoding='cp1252')
    except pd.errors.ParserError:
        df = strip_trail_commas(fname)
    return df

# Load dataframe to database
def load_to_database(dbase,dframe,additional_fields={}):
    for ind,row in dframe.iterrows():
        newDoc = dict(row)
        newDoc.update(additional_fields) # Add additional fields
        dbase.insert(newDoc)
    return dbase

# Main Function
def main():    
    keepCols = load_keep_columns("../Data/football-data-uk/colmap.txt")
    file_list = glob.glob("../Data/football-data-uk/*.csv")
    db = fdb.LoadDB()
    fduk = fdb.SetupTbl(db,'football-data-uk')
    for ind,f in enumerate(file_list):
        df = csv_to_dataframe(f)        
        df = df.filter(keepCols)
        load_to_database(fduk,df,{'Source':'football-data-uk','Season':strip_filename_season(f)})
        print(f"loading file ... {ind}/{len(file_list)}",end='\r',flush=True)
    print("Done")

if __name__ == '__main__':
    main()
