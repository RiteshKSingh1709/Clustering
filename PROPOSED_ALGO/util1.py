import math  
import random
import numpy as np
import sys
from PIL import Image, ImageDraw,ImageFont
from win32api import GetSystemMetrics
from Gene_vs_DataPoints import Corresponding_Gene,point_color

def importdata(filepath):
	t=open(filepath,'r')
	data=[]
	for line in t.readlines():
		data.append([float(i) for i in line.split()])
	return data

def proposed(data,no_clusters,e):
	print "STEPS:"

	#for data read#

	print "1.Data Fetched..."

	#Building the distance matrix and Calculation of DIFFERENCE and No of Buckets#  

	global distance_matrix
	from scipy.spatial.distance import pdist,squareform
	x=np.array(data,dtype=float)
	d=squareform(pdist(x,'euclidean'))
	MAX=np.amax(d)
	distance_matrix=d.tolist()

	print "2.Distance Matrix created..."
	for i in range(len(data)):
		d[i][i]=float('inf')
	MIN=np.amin(d)
	del d 
	diff=MAX-MIN
	print "\tDIFFERENCE:",diff,"\n\tMAXIMUM:",MAX,"\n\tMINIMUM:",MIN
	n=int(math.ceil((MAX)/100))
	print "\tNo of Buckets:",n

	#CREATING BUCKETS=[COUNT,AVERAGE,PROFIT]#
	#COUNT=No of distances that fall between a bucket range#

	bucket={}
	for i in range(0,n):
		bucket[i]=[0,0,0]            #initializing Bucket
	count_repeat=[]                  #for each bucket counts the repeation of datapoints in  
	for i in range(0,n):	         #distances that fall in between bucket range
		count_repeat.append([0 for j in range(len(data))])

	# the dimension of count_Repeat = [buckets][dimension_of_data]

	print "3.BUCKETS created..."
	#CALCULATION OF COUNT AND AVG FOR EACH BUCKET#

	for i in range(0,len(data)):
		count=0
		for j in range(i):
			if i==j:
				continue
			d=distance_matrix[i][j]
			# print "%8.2f  "%d,      #For printing Distance Matrix
			index=int(d/100)
			# print index
			try:
				count_repeat[index][i]+=1
			except IndexError:
				print index,"printed",n
			count_repeat[index][j]+=1
			bucket[index][0] += 1
			p = bucket[index][0]
			q = bucket[index][1]
			bucket[index][1] = (p*q + d)/(p+1)
		# print        #if you want print distance matrix ,uncomment this print

	print "4.COUNT AND AVG calculated..."

	#for PRINTING BUCKETS AND COUNT REPEAT

	print "\nBUCKETS:"
	for index,i in enumerate(bucket):
		if bucket[i][0]==0 or bucket[i][1]==0:
			continue
		bucket[i][2]=bucket[i][0]/bucket[i][1]


	#CALCULATION OF MAX PROFIT

	max_profit_bucket=0
	max_profit=0.0
	for i in bucket.iterkeys():
		if bucket[i][2]>max_profit:
			max_profit=bucket[i][2]
			max_profit_bucket=i 
	print "5.Max Profit calculated for each Bucket...\n\n"
	print "Max Profit:",max_profit,"\nBucket No. having Max Profit:",max_profit_bucket
	print "No of distances that fall in Max Profit Bucket:",bucket[max_profit_bucket][0]
	print "Average distance calculated in Max Profit Bucket:",bucket[max_profit_bucket][1] 

	sorted_profit_buckets=sorted(bucket.items(), key=lambda e: e[1][2])
	max_profit_list=[]
	for i in range(-1,-11,-1):
		# print sorted_profit_buckets[i][0],sorted_profit_buckets[i][1][0],sorted_profit_buckets[i][1][1],sorted_profit_buckets[i][1][2]
		max_profit_list.append(sorted_profit_buckets[i])
	print "max_profit_list:",max_profit_list
	# no_clusters=raw_input("Enter the no of clusters:")
	minimized_count_repeat=[]
	for i in range(0,n):
		m={}
		for j in range(0,len(data)):
			if count_repeat[i][j]==0:
				continue
			else:
				m[j]=count_repeat[i][j]
		minimized_count_repeat.append(m)
	print "Minimization done."
	it=0
	mincost=float('inf')
	best_cls=[]
	best_cluster=[]
	while(it<e) :
		print "iterations:",it
		clusters = []
		# selected_points = []
		# count=0
		# clusters=[]
		# while count<no_clusters:
		# 	highest_count=0		
		# 	for i in range(0,len(max_profit_list)):
		# 		k=max_profit_list[i][0] #bucket number
		# 		for j in minimized_count_repeat[k].iterkeys():
		# 			if (minimized_count_repeat[k][j]>highest_count) and (j not in selected_points):
		# 				highest_count=minimized_count_repeat[k][j]
		# 				highest_neighbour_bucket=k
		# 				highest_neighbour_point=j
		# 	selected_points.append(highest_neighbour_point)
		# 	clusters.append(highest_neighbour_point)

		# 	# for i in range(0,len(max_profit_list)):
		# 	# 	k=max_profit_list[i][0]
		# 	# 	check=minimized_count_repeat[k].get(highest_neighbour_point,"0")
		# 	# 	if check=="0":
		# 	# 		continue
		# 	# 	minimized_count_repeat[k][highest_neighbour_point]=0

		# 	count+=1
		clusters = inital_cluster_center_selection(max_profit_list,minimized_count_repeat,distance_matrix,diff)
		c=np.array(clusters)
		print c
		cost,cls=calculate_cost(data,no_clusters,c)
		if cost<mincost:
			mincost=cost
			best_cls=cls
			best_cluster=clusters
		it+=1
	return best_cls,best_cluster

def inital_cluster_center_selection(max_profit_list,minimized_count_repeat,distance_matrix,diff):
	count = 0
	selected_points = []
	cluster_center = []
	while count < 3:
		highest_count = 0 
		for i in range(0,len(max_profit_list)):
			k = max_profit_list[i][0] #k : lbucket number
			for j in minimized_count_repeat[k].iterkeys():
				if minimized_count_repeat[k][j] > highest_count and (j not in selected_points):
					if len(selected_points) > 1:
						for l in selected_points:
							if distance_matrix[l][j] > 2*diff:
								temp_cluster_center = j
								highest_count = minimized_count_repeat[k][j]
					else:
						temp_cluster_center = j
						highest_count = minimized_count_repeat[k][j]
		cluster_center.append(temp_cluster_center)
		selected_points.append(temp_cluster_center)
		count += 1

	return cluster_center

def calculate_cost(points, k,node):
    N = len(points)
    d_mat = np.asmatrix(np.empty((k,N)))
    d_mat = fill_distances(d_mat, points, node)     
    cls = assign_to_closest(points, node, d_mat) 
    cost = total_dist(d_mat, cls,node)
    return cost,cls
    
    
def dist_euc(vector1, vector2):
    dist = 0
    for i in range(len(vector1)):
        dist += (vector1[i] - vector2[i])**2
    return math.sqrt(dist)

def assign_to_closest(points, meds, d_mat):
    cluster =[]
    for i in xrange(len(points)):
        if i in meds:
            cluster.append(np.where(meds==i))
            continue
        d = sys.maxint
        idx=i
        for j in xrange(len(meds)):
            d_tmp = d_mat[j,i]
            if d_tmp < d:
                d = d_tmp
                idx=j
        cluster.append(idx)
    return cluster


def fill_distances(d_mat, points, current_node):
    for i in range(len(points)):
        for k in range(len(current_node)):
			d_mat[k,i]=dist_euc(points[current_node[k]], points[i])
	return d_mat
        
        
def total_dist(d_mat, cls,node):
	# print cls

    tot_dist = 0
    for i in xrange(len(cls)):
    	print "cls[i] :",cls[i]
    	if i in node:
    		continue
        tot_dist += d_mat[cls[i],i]
    return tot_dist


def update_distances(d_mat, points, node, idx):
    for j in range(len(points)):
        d_mat[idx,j]=dist_euc(points[node[idx]], points[j])

