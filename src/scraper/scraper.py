#!/usr/bin/python
# coding: utf-8

# In[81]:

from pymongo import MongoClient
import pymongo
import riotwatcher as rw
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
import time
import progressbar
from optparse import OptionParser
import json

# In[82]:

DATA_DB = "data"
GAME_TABLE = "games"
SUMMONER_TABLE = "summoners"
QUEUES = "queues"
GAME_QUEUE = "game_queue"
SUMMONER_QUEUE = "summoner_queue"
QUEUE_NAME = "summoner_queue"
URL = "192.168.5.100"
REGION = rw.NORTH_AMERICA

BRONZE_QUEUE = "bronze_summoners"
SILVER_QUEUE = "silver_summoners"
GOLD_QUEUE = "gold_summoners"
PLAT_QUEUE = "plat_summoners"
DIAMOND_QUEUE = "diamond_summoners" 
PRO_QUEUE = "master/challenger_summoners"

BRONZE = "BRONZE"
SILVER = "SILVER"
GOLD = "GOLD"
PLAT = "PLAT"
DIAMOND = "DIAMOND"
MASTER = "MASTER"
CHALLENGER = "CHALLENGER"

# frodo621 key: 
# 45fbe47f-84f1-43b6-9394-9f433a23d522


# In[143]:

class MongoDBQueue:
    def __init__(self, db, collection, url="127.0.0.1", port="27017"):
        self.url = url
        self.port = port
        self.db = db
        self.collection = collection
        self.connection = MongoClient("mongodb://"+url+":"+port)
        
        self.queue = self.connection[self.db][self.collection]
        
    def pop(self):
        return self.queue.find_one_and_delete({},None,[("_id",pymongo.ASCENDING)])["id"]
        #return self.connection[self.db].command("findandmodify", self.collection, query = {}, sort = {"_id": pymongo.ASCENDING}, remove=True)
        
    def push(self, i):
        check = self.queue.find_one({"id":i})
        if check == None:
            self.queue.insert({"id":i})
            return True
        return False
        #return self.connection[self.db].command("insert", self.collection, doc)

db_summoner_queue = MongoDBQueue(QUEUES, SUMMONER_QUEUE)
db_game_queue = MongoDBQueue(QUEUES, GAME_QUEUE)

db_tier_queues = {
    BRONZE:   MongoDBQueue(QUEUES, BRONZE_QUEUE),
    SILVER:   MongoDBQueue(QUEUES, SILVER_QUEUE),
    GOLD:     MongoDBQueue(QUEUES, GOLD_QUEUE),
    PLAT:     MongoDBQueue(QUEUES, PLAT_QUEUE),
    DIAMOND:  MongoDBQueue(QUEUES, DIAMOND_QUEUE),
    MASTER:     MongoDBQueue(QUEUES, PRO_QUEUE),
    CHALLENGER: MongoDBQueue(QUEUES, PRO_QUEUE)
}  


# In[136]:

class MongoDBSafe:
    def __init__(self, db, collection, url="127.0.0.1", port="27017"):
        self.url = url
        self.port = port
        self.db = db
        self.collection = collection
        self.connection = MongoClient("mongodb://"+url+":"+port)
        
    def push(self, doc):
        return self.connection[self.db][self.collection].insert(doc)
    
    def get(self, doc):
        return self.connection[self.db][self.collection].find_one(doc)
    
db_games_table = MongoDBSafe(DATA_DB, GAME_TABLE)
db_summoners_table = MongoDBSafe(DATA_DB, SUMMONER_TABLE)


# In[141]:

def wait_for_request():
    while not watcher.can_make_request():
        time.sleep(0.1)

def get_summoners_from_queue(num, queue):
    # replace with a single query
    for i in range(0,num):
        summoner_queue.append(queue.pop())
    
def query_summoner(summoner_id):
    print "query summoner"
    # get the basic information for that summoner
    wait_for_request()
    try:
        summoner_info = watcher.get_summoner( _id = summoner_id )
        db_summoners_table.push(summoner_info)
        
        # get the match history for that summoner
        # TO DO: scrape more matches per summoner
        wait_for_request()
        match_history = watcher.get_match_history(summoner_id, 
                                                  region=REGION, 
                                                  champion_ids = None, 
                                                  ranked_queues=rw.solo_queue,
                                                  begin_index=None,
                                                  end_index=None)
        
        # get the matches in that history and push them onto the queue
        match_ids = map(lambda x: x["matchId"], match_history["matches"])
        for match_id in match_ids:
            if not db_games_table.get({"_id":match_id}):
                game_queue.append(match_id)
    except LoLException as error:
        print "ERROR: ", error.error
        
        
    
def scrape_game(match_id):
    print "scraping game"
    # get match data using riot api
    wait_for_request()
    try:
        match_data = watcher.get_match(match_id, region=REGION, include_timeline=True)
        # add in _id field
        match_data["_id"] = match_data["matchId"]
        
        
        # push the game data to the database
        db_games_table.push(match_data)
        
        # find summoners in the match and push them to the queue
        player_ids = map(lambda x: (x["player"]["summonerId"], x["participantId"]) , match_data["participantIdentities"])
        tiers = {x["participantId"]: x["highestAchievedSeasonTier"] for x in match_data['participants']}
        for sum_id, part_id in player_ids:
            queue = db_tier_queues[tiers[part_id]]
            queue.push(sum_id)

    except LoLException as error:
        print "ERROR: ", error.error
    

# In[72]:
parser = OptionParser()
parser.add_option("-s","--seed", dest = "seedfile", default=False)
parser.add_option("-k","--key", dest = "key", default = False)
parser.add_option("-g", "--games", dest="games", default = 10000)
(options, args) = parser.parse_args()

if(options.seedfile):
	with open(options.seedfile) as f:
		seeds = json.load(f)
            for tier in seeds.keys():
                for sum_id in seeds[tier]:
                    db_summoner_queue.push(sum_id)


target_num = int(options.games)

if(options.key):
	key = options.key
else:
	key = raw_input("Please enter your Riot key: ")

watcher = RiotWatcher(key)


game_queue = []
summoner_queue = []
games_scraped = 0

tier = 0
while games_scraped < target_num:
    if len(summoner_queue) == 0 and len(game_queue) == 0:
        next_queue = db_tier_queues[db_tier_queues.keys()[tier]]
        print next_queue, db_tier_queues.keys()[tier]
        get_summoners_from_queue(1, next_queue)
        tier = (tier+1)%6
    if len(game_queue) == 0:
        query_summoner(int(summoner_queue.pop()))
    if len(game_queue) > 0:
        scrape_game(game_queue.pop())
        games_scraped += 1
        print games_scraped
        
