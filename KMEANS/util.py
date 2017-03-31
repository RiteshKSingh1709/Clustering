import random
import math
import gc
from PIL import Image,ImageDraw,ImageFont
from win32api import GetSystemMetrics
from Gene_vs_DataPoints import Corresponding_Gene,point_color


# Global variables
no_change = {}
#utility


def euclidean_distance(vector1, vector2):
	dist = 0
	for i in range(len(vector1)):
		dist += (vector1[i] - vector2[i])**2
	return(math.sqrt(dist))


def calculate_mean(data_points,num_dimension,data):
	mean=[]
	
	for k in range(num_dimension):
		sum=0.0
		for j in data_points:
			sum+=data[j][k]
		mean.append(float(sum/len(data_points)))
	return mean
	
def kmeans(cluster_centre,k,num_dimension,data):
	clusters={}

	for j in cluster_centre:
			clusters[j] = []

	for i in range(len(data)):
		min_cost = float('inf')
		for j in cluster_centre:
			temp = euclidean_distance(data[j],data[i])
			if temp < min_cost:
				min_cost = temp
				nearest_cluster= j
		clusters[nearest_cluster].append(i)

	mean={}
	for index,i in enumerate(clusters):
			mean[index]=calculate_mean(clusters[i],num_dimension,data)

	it=0
	while not no_change['status']:
		near_to_mean={}
		for j in mean.iterkeys():
			near_to_mean[j] = []
		for i in range(len(data)):
			min=float('inf')
			for k in mean.iterkeys():
				x=euclidean_distance(mean[k],data[i])
				# print"d[%d]-c[%d]"%(i,k),x
				if x<min:
					min=x
					nearest_cluster=k
			near_to_mean[nearest_cluster].append(i)

		# to check if there is no change...!!
		for index,i in enumerate(near_to_mean):
			if no_change[index] != len(near_to_mean[i]):
				no_change['status'] = False
				for index,i in enumerate(near_to_mean):
					no_change[index] = len(near_to_mean[i])
				break
			else:
				no_change[index] = len(near_to_mean[i])
				no_change['status'] = True

		print "%d"%it,
		for i in near_to_mean.iterkeys():
			print len(near_to_mean[i]),

		it+=1
		print "\n"
		for index,i in enumerate(near_to_mean):
			mean[index]=calculate_mean(near_to_mean[i],num_dimension,data)

     
	return near_to_mean

def init(filename,k):
	t=open(filename)
	data=[]
	for line in t.readlines():
		data.append([float(i) for i in line.split()])

	for i in range(k):
		no_change[i] = 0
	no_change['status'] = False
	return data

	
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

def create_cluster_image(cluster_item):
	

	# plotiing the cluster..!!

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


	for j in cluster_item.iterkeys():
		for k in cluster_item[j]:
			plot(draw,coordinate_tuple[j],j,centre[j],radius[j],k)

	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 20)
	font2=ImageFont.truetype("fonts/OpenSans-Bold.ttf", 15)
	for i,key in enumerate(cluster_item):
	    s="CLUSTER "+str(i)
	    s1="   ("+str(len(cluster_item[key]))+")"
	    draw.text((coordinate_tuple[i][0]+140, coordinate_tuple[i][3]+25),s,(0,0,0),font=font)
	    draw.text((coordinate_tuple[i][0]+160, coordinate_tuple[i][3]+50),s1,(200,0,0),font=font2)


	img = Image.open('images/kmeans.png', 'r')
	im.paste(img,(390,560))

	return im

def clear_mem():
	gc.collect()
	
