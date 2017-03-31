import numpy as np
import math
from PIL import Image, ImageDraw,ImageFont
from win32api import GetSystemMetrics
import random
from Gene_vs_DataPoints import Corresponding_Gene,point_color

degree_of_memb=[]
data=[]
cluster_centre=[]
count=0
def init(filename,c,dp,d,f,e):
    
    global num_data_points
    global num_clusters
    global num_dimensions
    global fuzziness
    global epsilon
    num_data_points=int(dp)
    num_clusters=int(c)
    num_dimensions=int(d)
    fuzziness=float(f)
    epsilon=float(e)
    global data
    global cluster_centre
    data=[]
    cluster_centre=[]
    
    count=0
    t=open(filename)
    for line in t.readlines():
        data.append([i for i in line.split()])
    

    for j in range(0,num_clusters):
        cluster_centre.append([])
        for k in range(0,num_dimensions):
            cluster_centre[j].append(0.0)

def init_degree_of_memb(num_data_points,num_clusters):
    for i in range(0,num_data_points):
        s,r=0.0,100.0
        degree_of_memb.append([])
        degree_of_memb[i].append(0.0)
        for j in range(1,num_clusters):
            rval=random.random()%(r+1)
            r-=rval
            degree_of_memb[i].append(float(rval/100.0))
            s+=degree_of_memb[i][j]
        degree_of_memb[i][0]=1.0-s
    return degree_of_memb

def restore_degree_of_memb(memb_matrix):
    degree_of_memb=memb_matrix
    
        

def calculate_centre_vectors():
    t=np.power(np.array(degree_of_memb,dtype=float),fuzziness).tolist()
    global count
    count+=1
    print "Iterations:",count
    for j in range(0,num_clusters):
        for k in range(0,num_dimensions):
            numerator=0.0
            denominator=0.0
            for i in range(0,num_data_points):
                numerator+=t[i][j]*float(data[i][k])
                denominator+=t[i][j]
            cluster_centre[j][k]=float(numerator/denominator)
       
def get_norm(i,j):
    sum=0.0
    for k in range(0,num_dimensions):
        sum+=math.pow((float(data[int(i)][k])-cluster_centre[int(j)][k]),2)
    return math.sqrt(sum)

def get_new_value(i,j):
    sum=0.0
    p=2/(fuzziness-1)
    for k in range(0,num_clusters):
        t=get_norm(int(i),int(j))/get_norm(int(i),int(k))
        t=math.pow(t,p)
        sum+=t
    return 1.0/sum

def update_degree_of_membership():
    max_diff=0.0
    for j in range(0,num_clusters):
        for i in range(0,num_data_points):
            new_uij=get_new_value(i,j)
            diff=new_uij - degree_of_memb[i][j]
            if diff>max_diff:
                max_diff=diff
            degree_of_memb[i][j]=new_uij
    
    return max_diff        

def fcm(filename,num_clusters,num_data_points,num_dimensions,fuzziness,epsilon):
    max_diff=0.0
    init(filename,num_clusters,num_data_points,num_dimensions,fuzziness,epsilon)
    calculate_centre_vectors()
    max_diff=update_degree_of_membership()
    while max_diff>epsilon:
        calculate_centre_vectors()
        max_diff=update_degree_of_membership()
    return degree_of_memb


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


    # font = ImageFont.truetype("fonts/Ficticcia College.otf", 45)
    # draw.text((420,600),"FUZZY-C-MEANS CLUSTERING",(165,42,42),font=font)   
    img = Image.open('images/fcm.png', 'r')
    im.paste(img,(390,560))

    return im






