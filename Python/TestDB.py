import FootballDB as fdb
import pprint

db = fdb.Load()
db.insert({'type':'Match','country':'England','division':'Premier League','id':1})
db.insert({'type':'Match','country':'England','division':'Premier League','id':2})
pprint.pprint(db.all())
db.purge()
