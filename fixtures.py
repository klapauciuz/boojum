import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['boojom']
db.tags.insert([
    {"name":"green"},
    {"name":"white"},
    {"name":"red"},
    {"name":"blue"},
    {"name":"black"}
])
db.objects.insert([
    {"name":"The Shawshank Redemption"},
    {"name":"The Green Mile"},
    {"name":"Forrest Gump"},
    {"name":"Schindler's List"},
    {"name":"Intouchables"}
])
