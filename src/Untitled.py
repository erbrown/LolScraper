
# coding: utf-8

# In[2]:

from pymongo import MongoClient
import pymongo


# In[5]:

QUEUES = "queues"
GAME_QUEUE = "game_queue"
SUMMONER_QUEUE = "summoner_queue"
QUEUE_NAME = "summoner_queue"
URL = "192.168.5.100"


# In[6]:

client = MongoClient('mongodb://'+URL)
client[QUEUES][GAME_QUEUE].insert({"matchId":1822103434})
client[QUEUES][SUMMONER_QUEUE].insert({ "id":23376539 })


# In[ ]:



