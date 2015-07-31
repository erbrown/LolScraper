from bson.code import Code
from pymongo import MongoClient
import pymongo
import json
import time

start_time = time.time()

URL = "98.216.209.75"

db  = MongoClient("mongodb://"+URL+":27017")

map_js = Code(open('fb_map.js', 'r').read())
reduce_js = Code(open('fb_reduce.js','r').read())

results = db['data']['games'].map_reduce(map_js, reduce_js, 'fb_results')
print start_time - time.time(), "seconds"
print results

#for result in results.find():
#	print result['_id']

#results_json = json.dumps(results)
#with open('fb_data.json', 'wb') as f:
#	f.write(results_json)

