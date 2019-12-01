from tinydb import TinyDB, Query
import pandas as pd

# Setup Database
def SetupDB():
    db = TinyDB('../Data/db/footballdb.json')
    db.purge()
    return db

# Setup Table
def SetupTbl(dbase,tableName):
    if tableName in dbase.tables():
        dbase.purge_table(tableName)
    return dbase.table(tableName)

# Load Database
def LoadDB():
    db = TinyDB('../Data/db/footballdb.json')
    return db

# Load Table
def LoadTbl(dbase,tableName):
    return dbase.table(tableName)

# Load Dataframe
def LoadDframe(data):
    return pd.DataFrame(data)

# Print Dataframe
def ExportDframe(df,file_path="../Analysis/Analysis.csv"):
    df.to_csv(file_path)
