import numpy as np
import random,math
from PIL import Image, ImageDraw,ImageFont
from win32api import GetSystemMetrics
import sklearn.cluster
from Gene_vs_DataPoints import Corresponding_Gene,point_color

def agglomerative(file_name,k):
    t=open(file_name)
    data=[]
    for line in t.readlines():
    	data.append([float(i) for i in line.split()])

    X=data
    from sklearn.neighbors import kneighbors_graph
    knn_graph = kneighbors_graph(X, 30, include_self=False)

    from sklearn.cluster import AgglomerativeClustering
    model = AgglomerativeClustering(linkage='ward',connectivity=knn_graph,n_clusters=k)
    x=model.fit_predict(X).tolist()
    cluster = {0:[],1:[],2:[]}	
    j=0
    for i in x:
        if i==0:
            cluster[i].append(j)
        if i==1:
            cluster[i].append(j)
        if i==2:
            cluster[i].append(j)
        j=j+1
    return cluster


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


def create_cluster_image(cluster):
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

    for j in cluster.iterkeys():
    	for k in cluster[j]:
    		plot(draw,coordinate_tuple[j],j,centre[j],radius[j],k)

    font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 20)
    font2=ImageFont.truetype("fonts/OpenSans-Bold.ttf", 15)
    for i in cluster.iterkeys():
        s="CLUSTER "+str(i)
        s1="   ("+str(len(cluster[i]))+")"
        draw.text((coordinate_tuple[i][0]+140, coordinate_tuple[i][3]+25),s,(0,0,0),font=font)
        draw.text((coordinate_tuple[i][0]+160, coordinate_tuple[i][3]+50),s1,(200,0,0),font=font2)

    # font = ImageFont.truetype("fonts/Aller_Bd.ttf", 45)
    # draw.text((420,600),"AGGLOMERATIVE CLUSTERING",(153,153,0),font=font)
    img = Image.open('images/agglo.png', 'r')
    im.paste(img,(300,560))	

    return im
