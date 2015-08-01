from pymongo import MongoClient
import pymongo
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread

db = MongoClient("mongodb://98.216.209.75:27017")

def data_to_mini_ig(data):
	map()

results = db['data']['fb_results'].find()

print results[0]['value']['x']

results = filter(lambda x: x['value']['x'] is not 0 and x['value']['y'] is not 0, results)

x_vals = map(lambda a: float(a['value']['x']), results)
y_vals = map(lambda a: float(a['value']['y']), results)

heatmap, xedges, yedges = np.histogram2d(x_vals, y_vals, bins=50, range=[[0,14820],[0,14881]])
extent = [-120, 14870, -120, 14980]


colors = [(0,0,0),'b','r']
cmap = mpl.colors.LinearSegmentedColormap.from_list('color map', colors)

summoners_rift = imread("minimap-ig.jpg")

plt.clf()

#plt.scatter(x_vals, y_vals)
plt.imshow(heatmap, extent=extent, cmap=cmap, alpha=0.8, zorder=1)


plt.imshow(summoners_rift, extent=extent, aspect='auto', zorder=0, origin='lower')

plt.gca().invert_yaxis()


plt.show()
