import util
import random,math
import sys
import time
from PIL import Image, ImageDraw,ImageFont
from win32api import GetSystemMetrics
from Gene_vs_DataPoints import Corresponding_Gene,point_color
import numpy as np



# Global variables
initMedoidsFixed = False # Fix the init value of medoids for performance comparison
debugEnabled = True # Debug
distances_cache = {}	# Save the tmp distance for acceleration (idxMedoid, idxData) -> distance
distance_matrix=[]
def init(filePath):

	data = []
	try:
		fnObj = open(filePath, 'r')
		for line in fnObj:
			line = line.strip().split()
			point = []
			for c in line:
				point.append(float(c))
			data.append(tuple(point))
	finally:
		fnObj.close()
	
	return(data)

 
def totalCost(data, medoids_idx,cacheOn=False):
	
	#Compute the total cost and do the clustering based on certain cost function
	
	
	# Init the cluster
	size = len(data)
	total_cost = 0.0
	medoids = {}
	for idx in medoids_idx:
		medoids[idx] = []

	for i in range(size):
		choice = -1
		# Make a big number
		min_cost = float('inf')
		for m in medoids:
			if cacheOn == True:
				# Check for cache
				tmp = distances_cache.get((m,i), None)
			if cacheOn == False or tmp == None:
				# euclidean_distance
				tmp = distance_matrix[m][i]
				
			if cacheOn == True:
				# Save the distance for acceleration
				distances_cache[(m,i)] = tmp
			# Clustering
			if tmp < min_cost:
				choice = m
				min_cost = tmp
		# Done the clustering
		medoids[choice].append(i)
		total_cost += min_cost
	
	# Return the total cost and clustering
	return(total_cost, medoids)
     
 
def kmedoids(data, k):
	
	#kMedoids - PAM implemenation
	#See more : http://en.wikipedia.org/wiki/K-medoids
	#The most common realisation of k-medoid clustering is the Partitioning Around Medoids (PAM) algorithm and is as follows:[2]
	#1. Initialize: randomly select k of the n data points as the medoids
	#2. Associate each data point to the closest medoid. ("closest" here is defined using any valid distance metric, most commonly Euclidean distance, Manhattan distance or Minkowski distance)
	#3. For each medoid m
	#	For each non-medoid data point o
	#		Swap m and o and compute the total cost of the configuration
	#4. Select the configuration with the lowest cost.
	#5. repeat steps 2 to 4 until there is no change in the medoid.
	global distance_matrix
	from scipy.spatial.distance import pdist,squareform
	x=np.array(data,dtype='float32')
	d=squareform(pdist(x,'euclidean'))
	distance_matrix=d.tolist()
	del d
	
	size = len(data)
	medoids_idx = []
	if initMedoidsFixed == False:
		medoids_idx = random.sample([i for i in range(size)], k)
	else:
		medoids_idx = [i for i in range(k)]
	pre_cost, medoids = totalCost(data, medoids_idx)
	if debugEnabled == True:
		print('pre_cost: ', pre_cost)
		#print('medioids: ', medoids)
	current_cost = pre_cost
	best_choice = []
	best_res = {}
	iter_count = 0

	while True:
		for m in medoids:
			for item in medoids[m]:
				# NOTE: both m and item are idx!
				if item != m:
					# Swap m and o - save the idx
					idx = medoids_idx.index(m)
					# This is m actually...
                    			swap_temp = medoids_idx[idx]
                    			medoids_idx[idx] = item
                    			tmp_cost, tmp_medoids = totalCost(data, medoids_idx)
					# Find the lowest cost
                    			if tmp_cost < current_cost:
						best_choice = list(medoids_idx) # Make a copy
                        			best_res = dict(tmp_medoids) 	# Make a copy
                        			current_cost = tmp_cost
					# Re-swap the m and o
					medoids_idx[idx] = swap_temp
		# Increment the counter
		iter_count += 1
		if debugEnabled == True:
			print('current_cost: ', current_cost)
			print('iter_count: ', iter_count)

		if best_choice == medoids_idx:
			# Done the clustering
			break

		# Update the cost and medoids
		if current_cost <= pre_cost:
			pre_cost = current_cost
			medoids = best_res
			medoids_idx = best_choice

	return(current_cost, best_choice, best_res)

def create_point_inside_circle(coordinate_tuple,centre,radius):
    while True:
        x=random.randint(int(coordinate_tuple[0]+4),int(coordinate_tuple[2]-4))
        y=random.randint(int(coordinate_tuple[1]+4),int(coordinate_tuple[3]-4))
        r=math.sqrt((x-centre[0])**2+(y-centre[1])**2)
        if(r<radius):
            break
    return x,y


def plot(draw,coordinate_tuple,j,centre,radius,k):
    x,y=create_point_inside_circle(coordinate_tuple,centre,radius)
    if j==0:
    	draw.ellipse((x-4,y-4,x+4,y+4), fill =point_color[k],outline ='black')
    if j==1:
    	draw.ellipse((x-4,y-4,x+4,y+4), fill =point_color[k],outline ='black')
    if j==2:
    	draw.ellipse((x-4,y-4,x+4,y+4), fill =point_color[k],outline ='black')

def create_cluster_image(best_medoids): 
	
	
	Width = GetSystemMetrics(0)
	Height = GetSystemMetrics(1)
	im = Image.new("RGB",(Width,Height),"white")
	draw = ImageDraw.Draw(im)
	coordinate_tuple = [(45,45,405,405),(500,45,860,405),(955,45,1315,405)]
	centre=[]
	radius=[]
	for i in range(len(coordinate_tuple)):
	    l=[]
	    cx=(coordinate_tuple[i][0]+coordinate_tuple[i][2])/2
	    cy=(coordinate_tuple[i][1]+coordinate_tuple[i][3])/2
	    r=(coordinate_tuple[i][3]-coordinate_tuple[i][1])/2
	    l.append(cx)
	    l.append(cy)
	    centre.append(l)
	    radius.append(r)

	draw.ellipse((coordinate_tuple[0][0]-10,coordinate_tuple[0][1]-10,coordinate_tuple[0][2]+10,coordinate_tuple[0][3]+10),fill=(255,255,204),outline='black')
	draw.ellipse((coordinate_tuple[1][0]-10,coordinate_tuple[1][1]-10,coordinate_tuple[1][2]+10,coordinate_tuple[1][3]+10),fill='#E5FFCC',outline='black')
	draw.ellipse((coordinate_tuple[2][0]-10,coordinate_tuple[2][1]-10,coordinate_tuple[2][2]+10,coordinate_tuple[2][3]+10),fill='#CCE5FF',outline='black')


	for index,key in enumerate(best_medoids):
		for k in best_medoids[key]:
			plot(draw,coordinate_tuple[index],index,centre[index],radius[index],k)

	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 20)
	font2=ImageFont.truetype("fonts/OpenSans-Bold.ttf", 15)
	for i,key in enumerate(best_medoids):
	    s="CLUSTER "+str(i)
	    s1="   ("+str(len(best_medoids[key]))+")"
	    draw.text((coordinate_tuple[i][0]+140, coordinate_tuple[i][3]+25),s,(0,0,0),font=font)
	    draw.text((coordinate_tuple[i][0]+160, coordinate_tuple[i][3]+50),s1,(200,0,0),font=font2)

	# font = ImageFont.truetype("fonts/Aller_Bd.ttf", 45)
	# draw.text((490,600),"K-MEDOIDS CLUSTERING",(106,92,225),font=font)	
	img = Image.open('images/kmedoid.png', 'r')
	im.paste(img,(390,560))
	return im
