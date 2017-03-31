import numpy as np
t=open("diseased.txt")
data=[]
for line in t.readlines():
	data.append([float(i) for i in line.split()])

data_points=np.array(data,dtype=float)
h=data_points.max(axis=0).tolist()
l=data_points.min(axis=0).tolist()
Difference=list(np.array(h)-np.array(l))
del data_points
print " DIMENSION\t\tMAX VAL\t\tMIN VAL\t\tDIFFERENCE"
for i in range(len(h)):
	print "\t%d:"%i,"\t\t",h[i],"\t",l[i],"\t",Difference[i]

print "Maximum value:%f"%(max(h))
print "Minimum value:%f"%(min(l))
print "Maximum Difference:%f"%(max(Difference))
print "Minimum Difference:%f"%(min(Difference))

from scipy.spatial.distance import pdist,squareform
x=np.array(data,dtype='float32')
d=squareform(pdist(x,'euclidean'))
for i in range(len(d)):
	d[i][i]=float('inf')
print np.amin(d)
print min(distance_matrix)
