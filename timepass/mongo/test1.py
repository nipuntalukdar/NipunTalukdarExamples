import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.testdatabase
col = db.testcollection
col.insert({'FixedH': False,'Mstereo': True,'RecMet': False,'Sstereo': True,'bond': False,
            'charge': False, 'isotope': False,'length': 223,'nocomponents': 1,
            'nolayers': 6,'stereo': True})
cursor = col.find()
print 'Found', cursor.count()
print cursor.next()
client.close()

