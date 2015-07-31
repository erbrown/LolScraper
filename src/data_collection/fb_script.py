from pymongo.code import Code
import pymongo
import json

URL = "98.216.209.75"

connection  = pymongo.Connection()


map_js = Code(open('js/fb_map.js', 'r').read())
#reduce_js = Code(open('fb_reduce.js','r').read())

results = db.data.map(map_js)

for result in results.find():
	print result['_id'], result['value']['count']

results_json = json.dumps(results)
with open('fb_data.json', 'wb') as f:
	f.write(results_json)

