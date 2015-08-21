from bson.code import Code
from pymongo import MongoClient
import pymongo
import json
import time
import riotwatcher
from riotwatcher import RiotWatcher
from collections import defaultdict
from sklearn.decomposition import PCA
import numpy as np

start_time = time.time()

URL = "98.216.209.75"

db  = MongoClient("mongodb://"+URL+":27017")

item_map_js = Code(open('items/item_map.js', 'r').read())
champ_map_js = Code(open('champs/champ_map.js', 'r').read())

reduce_js = Code(open('sum_reduce.js','r').read())

#3724, 3720: runeglaive
AP_ITEMS = {3724:"Runeglaive",
			3089:"Rabadons",
			3720:"Runeglaive",
			3285:"Ludens Echo",
			3290:"Twin Shadows",
			3092:"Frost Queens",
			3716:"Runeglaive",
			1056:"Doran's Ring",
			3100:"Lich Bane",
			3504:"Ardent Censer",
			3708:"Runeglaive",
			2139:"Elixer of Sorcery",
			3146:"Hextech Gunblade",
			3003:"Archangel's Staff",
			3152:"Will of the Ancients",
			3151:"Liandry's Torment",
			3135:"Void Staff",
			3001:"Abyssal Scepter",
			3124:"Guinsoo's Rageblade",
			3027:"Rod of Ages",
			3025:"Iceborn Gauntlet",
			3115:"Nashor's Tooth",
			3116:"Rylais Crystal Scepter",
			3023:"Twin Shadows",
			3020:"Sorcerers Shoes",
			3050:"Zekes Harbinger",
			3041:"Mejais",
			3174:"Athenes",
			3158:"Ionian Boots",
			3157:"Zhonyas",
			3060:"Banner of Command",
			3165:"Morellonomicon"
		}

# frodo621 key: 
key = "45fbe47f-84f1-43b6-9394-9f433a23d522"
watcher = RiotWatcher(key)

#champ_data = watcher.

# key = ( patch, region, tier, champ )
# values = [ feature vector ]


final_data = defaultdict(lambda: [0]*len(AP_ITEMS))
games = {}

for patch in ["5.11", "5.14"]:
    for region in ["BR"]: #,"EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"]:
		#item_results = db['API_Challenge'][patch + "_" + region].map_reduce(item_map_js, reduce_js, patch + "_" + region + "Item_Freq")
		#champ_results = db['API_Challenge'][patch + "_" + region].map_reduce(champ_map_js, reduce_js, patch + "_" + region + '_Champs')

		item_results = db["API_Challenge"][patch + "_" + region + "Item_Freq"]
		champ_results = db["API_Challenge"][patch + "_" + region + "_Champs"]
		for e in item_results.find():
			k = e['_id']
			if k['item'] in AP_ITEMS.keys():
				index = AP_ITEMS.keys().index(int(k['item']))
				final_data[( k['patch'], k['region'], k['tier'], k['champ'] )] [index] += e['value']

		for c in champ_results.find():
			k = c['_id']
			final_data[( k['patch'], k['region'], k['tier'], k['champ'] )] = map( lambda x: float(x)/c['value'], final_data[( k['patch'], k['region'], k['tier'], k['champ'] )])
			games[( k['patch'], k['region'], k['tier'], k['champ'] )] = c['value']

print final_data[final_data.keys()[0]]

pca = PCA(n_components=2)

reduction = pca.fit_transform(final_data.values())

json_data = []
for i in range(0,len(final_data.keys())):
	key = final_data.keys()[i]
	data = list(reduction[i])
	num_games = games[key]
	json_data.append( {
		"patch":key[0],
		"region":key[1],
		"tier":key[2],
		"champion":key[3],
		"coordinate":{
			"x":data[0],
			"y":data[1]
		},
		"games":num_games
		}  )

with open("pca_dump.json", "w") as f:
	json.dump(json_data, f)

print(pca.explained_variance_ratio_)


print time.time() - start_time, "seconds"


