from util import xclarans,create_cluster_image
import sys
from PIL import Image, ImageDraw,ImageFont
from extract_original import gene
from Gene_vs_DataPoints import Corresponding_Gene



def main():
	k=int(raw_input("Enter the no of Clusters:"))
	data = []
	try:
		fnObj = open('./diseased.txt', 'r')
		for line in fnObj:
			line = line.strip().split()
			point = []
			for c in line:
				point.append(float(c))
			data.append(tuple(point))
	finally:
		fnObj.close()
	print "\n\n\t\t---:For Diseased:---"
	print "\t\t--------------------\n\n"
	cls,best_node=xclarans(data, 3, 30, c,k)
	cluster_diseased = {0:[],1:[],2:[]}	
	j=0
	for i in cls:
	    if i==0:
	        cluster_diseased[i].append(j)
	    if i==1:
	        cluster_diseased[i].append(j)
	    if i==2:
	        cluster_diseased[i].append(j)
	    j=j+1

	data = []
	try:
		fnObj = open('./normal.txt', 'r')
		for line in fnObj:
			line = line.strip().split()
			point = []
			for c in line:
				point.append(float(c))
			data.append(tuple(point))
	finally:
		fnObj.close()
	print "\n\n\t\t---:For Normal:---"
	print "\t\t--------------------\n\n"		
	cls,best_node=xclarans(data, 3, 30, c,k)
	cluster_normal = {0:[],1:[],2:[]}	
	j=0
	for i in cls:
	    if i==0:
	        cluster_normal[i].append(j)
	    if i==1:
	        cluster_normal[i].append(j)
	    if i==2:
	        cluster_normal[i].append(j)
	    j=j+1

	cluster_diseased_vs_normal={}
	for i in cluster_diseased.iterkeys():
		highest_match=0
		data_points_diseased=cluster_diseased[i]
		for j in cluster_normal.iterkeys():
			x=len(set(data_points_diseased) & set(cluster_normal[j]))
			if x>highest_match:
				highest_match=x
				Corresponding_cluster=j
		cluster_diseased_vs_normal[i]=cluster_normal[Corresponding_cluster]
		del cluster_normal[Corresponding_cluster]


	# show image
	im_diseased=create_cluster_image(cluster_diseased)
	im_normal=create_cluster_image(cluster_diseased_vs_normal)
	draw = ImageDraw.Draw(im_diseased)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For DISEASED",(0,0,255),font=font)
	draw = ImageDraw.Draw(im_normal)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For NORMAL",(0,0,255),font=font)
	im_diseased.show()
	im_normal.show() 
	im_diseased.save("XCLARANS_DISEASED.png")
	im_normal.save("XCLARANS_NORMAL.png") 
	#check true positive
	responsible=[]
	for i in range(0,k):
		x=set(cluster_diseased_vs_normal[i])-set(cluster_diseased[i])
		responsible.extend(x)
	print "No of Genes responsible for diseased:",len(responsible)
	responsible_gene_name=[]
	for i in responsible:
		responsible_gene_name.append(Corresponding_Gene[i])
	true_positive=list(set(responsible_gene_name) & set(gene))
	name_of_gene = open('gene_names.txt','w+')
	counter = 1

	for name in true_positive:
		if (counter % 6 ) == 0:
			name_of_gene.write('\n')
			n_string = name.ljust(15,' ')
			name_of_gene.write(n_string)
			counter = 2
		else:
			n_string = name.ljust(15,' ')
			name_of_gene.write(n_string)
			counter += 1


	print len(true_positive)
	x=(float(len(true_positive))/float(len(responsible_gene_name)))*100.0
	print x


if __name__ == '__main__':
	main()