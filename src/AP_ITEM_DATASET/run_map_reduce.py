from bson.code import Code
from pymongo import MongoClient
import pymongo
import json
import time
import riotwatcher
from riotwatcher import RiotWatcher
from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn.random_projection import GaussianRandomProjection
import numpy as np
from matplotlib import pyplot as plt