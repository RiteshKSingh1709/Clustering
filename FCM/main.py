import sys
from util import fcm,create_cluster_image,init_degree_of_memb,restore_degree_of_memb
from PIL import Image, ImageDraw,ImageFont
from extract_original import gene
from Gene_vs_DataPoints import Corresponding_Gene


def main():
	k=int(raw_input("Enter the no of Clusters:"))
	n=int(raw_input("Enter the no of Datapoints:"))
	
	f=float(raw_input("Enter Fuzziness:"))
	e=float(raw_input("Termination criterion:"))
	d=int(raw_input("Enter the no of Dimensions for DISEASED:"))
	memb_matrix=init_degree_of_memb(n,k)
 
	degree_of_memb_diseased=fcm("./diseased.txt",k,n,d,f,e)
	cluster_diseased={}
	for i in range(0,k):
		cluster_diseased[i]=[]
	for i in range(0,n):
		cluster=0
		highest=0.0
		for j in range(0,k):
		    if degree_of_memb_diseased[i][j]>highest:
		        highest=degree_of_memb_diseased[i][j]
		        cluster=j
		    else:
		        continue
		cluster_diseased[cluster].append(i)
	for i in cluster_diseased.iterkeys():
		print i,":",len(cluster_diseased[i])
	

	d=int(raw_input("Enter the no of Dimensions for NORMAL:"))
	restore_degree_of_memb(memb_matrix)
	degree_of_memb_normal=fcm("./normal.txt",k,n,d,f,e)
	cluster_normal={}
	for i in range(0,k):
		cluster_normal[i]=[]
	for i in range(0,n):
		cluster=0
		highest=0.0
		for j in range(0,k):
		    if degree_of_memb_normal[i][j]>highest:
		        highest=degree_of_memb_normal[i][j]
		        cluster=j
		    else:
		        continue
		cluster_normal[cluster].append(i)
	for i in cluster_normal.iterkeys():
		print i,":",len(cluster_normal[i])
	
	# matching clusters from diseased to normal    
	cluster_diseased_vs_normal={}
	for i in cluster_diseased.iterkeys():
		highest_match=0
		data_points_diseased=cluster_diseased[i]
		for j in cluster_normal.iterkeys():
			x=len(set(data_points_diseased) & set(cluster_normal[j]))
			print "cluster_diseased %d &"%i+"cluster_normal %d:"%j,x
			if x>highest_match:
				highest_match=x
				Corresponding_cluster=j
		cluster_diseased_vs_normal[i]=cluster_normal[Corresponding_cluster]
		del cluster_normal[Corresponding_cluster]
	for i in cluster_diseased_vs_normal.iterkeys():
		print i,":",len(cluster_diseased_vs_normal[i])


	# show image
	im_diseased=create_cluster_image(cluster_diseased)
	im_normal=create_cluster_image(cluster_diseased_vs_normal)
	draw = ImageDraw.Draw(im_diseased)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For DISEASED",(163,52,52),font=font)
	draw = ImageDraw.Draw(im_normal)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For NORMAL",(163,52,52),font=font)
	im_diseased.show()
	im_normal.show()
	im_diseased.save("Fuzzy_diseased.png")
	im_normal.save("Fuzzy_normal.png") 

	#check true positive
	responsible=[]
	for i in range(0,k):
		x=set(cluster_diseased_vs_normal[i])-set(cluster_diseased[i])
		responsible.extend(x)
	print "No of Genes responsible for diseased:",len(responsible)
	responsible_gene_name=[]
	for i in responsible:
		responsible_gene_name.append(Corresponding_Gene[i])
	true_positive=list(set(responsible_gene_name) & set(gene))
	print len(true_positive)
	x=(float(len(true_positive))/float(len(responsible_gene_name)))*100.0
	print x






if __name__ == '__main__':
	main()