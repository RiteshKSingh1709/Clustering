import random
t=open("Lung_carcinoma_ds.csv")
Corresponding_Gene={}
i=0
data_point=0
for line in t.readlines():
	if i==0 or i==1 or i==2 or line.split(",")[0]=='NULL':
		i+=1
		continue
	Corresponding_Gene[data_point]=line.split(",")[0]
	data_point+=1

def get_spaced_colors(n):
    max_value = 16581375 #255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
    
    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

point_color={}
count=0
color=get_spaced_colors(6672)
for i in range(0,data_point):
	point_color[i]=color[i]
	
