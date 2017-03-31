import math
import random
import numpy as np
import sys
from PIL import Image, ImageDraw,ImageFont
from win32api import GetSystemMetrics
from Gene_vs_DataPoints import Corresponding_Gene,point_color


"""
1. Input parameters numlocal and maxneighbor. Initialize i to 1, and mincost to a large number.
2. Set current to an arbitrary node in G_{n,k}
3. Set j to 1.
4. Consider a random neighbor S of current, and based on Equation (5) calculate the cost differential 
    of the two nodes.
5. If S has a lower cost, set current to S, and go to Step (3).
6. Otherwise, increment j by 1. If j<=maxneighbor,go to Step (4).
7. Otherwise, when j > maxneighbor, compare the cost of current with mincost. If the former is less than mincost, 
    set mincost to the cost of current, and set bestnode to current.
8. Increment i by 1. If i > numlocal, output bestnode and halt. Otherwise, go to Step (2).
"""

def clarans(points, numlocal, maxneighbor, mincost,k):
#    random.seed(1)
#    np.random.seed(1)
    i=1
    N = len(points)
    d_mat = np.asmatrix(np.empty((k,N)))
    local_best = []
    bestnode = []
    
    while i<=numlocal:
        #Step 2 - pick k random medoids from data points - medoids_nr from points
        node = np.random.permutation(range(N))[:k]
        fill_distances(d_mat, points, node)     
        cls = assign_to_closest(points, node, d_mat) 
        cost = total_dist(d_mat, cls)
        copy_node = node.copy()
        print copy_node
        print 'new start \n'
        #increase neighbor count
        j = 1 
        
        while j<=maxneighbor:
            #Step 4 - pick a random neighbor of current node - i.e change randomly one medoid
            #calculate the cost differential of the initial node and the random neighbor
            changing_node = copy_node.copy()
            idx = pick_random_neighbor(copy_node, N)
            update_distances(d_mat, points, copy_node, idx)            
            cls = assign_to_closest(points, copy_node, d_mat)   
            new_cost = total_dist(d_mat, cls)
            
            #check if new cost is smaller 
            if new_cost < cost:
                cost = new_cost
                local_best = copy_node.copy()
                print 'Best cost: ' + str(cost) + ' '
                print local_best 
                print '\n'
                j = 1
                continue
            else:
                #copy_node = changing_node
                j=j+1
                if j<=maxneighbor:
                    continue
                elif j>maxneighbor:
                    if mincost>cost:
                        mincost = cost
                        print "change bestnode " 
                        print bestnode
                        print " into"
                        bestnode = local_best
                        print bestnode
                        print '\n'
                        
            i = i+1
            if i>numlocal:
                fill_distances(d_mat, points, bestnode)     
                cls = assign_to_closest(points, bestnode, d_mat)
                print "Final cost: " + str(mincost) + ' '
                print bestnode 
                print '\n'
                return cls, bestnode
            else:
                break
    
    
def pick_random_neighbor(current_node, set_size):
    #pick a random item from the set and check that it is not selected
    node = random.randrange(0, set_size, 1)
    while node in current_node:
        node = random.randrange(0, set_size, 1)
        
    #replace a random node
    i = random.randrange(0, len(current_node))
    current_node[i]=node
    return i
    
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
        
        
def total_dist(d_mat, cls):
    tot_dist = 0
    for i in xrange(len(cls)):
        tot_dist += d_mat[cls[i],i]
    return tot_dist


def update_distances(d_mat, points, node, idx):
    for j in range(len(points)):
        d_mat[idx,j]=dist_euc(points[node[idx]], points[j])

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
    # draw.text((490,600),"CLARANS CLUSTERING",(162,62,62),font=font)   
    img = Image.open('images/CLARANS.png', 'r')
    im.paste(img,(390,560)) 

    
    return im
