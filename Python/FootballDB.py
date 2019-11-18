from tinydb import TinyDB, Query

# Setup Database
def Setup():
    db = TinyDB('../Data/db/footballdb.json')
    db.purge()
    return db

# Load Database
def Load():
    db = TinyDB('../Data/db/footballdb.json')
    return db
