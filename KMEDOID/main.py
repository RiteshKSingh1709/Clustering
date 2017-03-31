from util import init,kmedoids,create_cluster_image,debugEnabled
import sys
import time
from PIL import Image, ImageDraw,ImageFont
from extract_original import gene
from Gene_vs_DataPoints import Corresponding_Gene



def main(): 

	k = int(raw_input("Enter the no of Clusters:"))
	if debugEnabled == True:
		print('k: ', k)


	# for diseased
	diseased = init("./diseased.txt")
	print "KMEDOIDS Clustering for Diseased"
	startTime = time.time()
	print time.asctime( time.localtime(time.time()) )
	best_cost_diseased, best_choice_diseased, best_medoids_diseased = kmedoids(diseased, k)
	endTime = time.time()
	print time.asctime( time.localtime(time.time()) )
	print('best_time: ', endTime - startTime)
	print('best_cost: ', best_cost_diseased)
	print('best_choice: ', best_choice_diseased)
	cluster_diseased={}
	for index,key in enumerate(best_medoids_diseased):
		cluster_diseased[index]=best_medoids_diseased[key]
	del diseased[:]


    # for normal
	normal = init("./normal.txt")
	startTime = time.time()
	print time.asctime( time.localtime(time.time()) )
	best_cost_normal, best_choice_normal, best_medoids_normal = kmedoids(normal, k)
	endTime = time.time()
	print time.asctime( time.localtime(time.time()) )
	print('best_time: ', endTime - startTime)
	print('best_cost: ', best_cost_normal)
	print('best_choice: ', best_choice_normal)
	cluster_normal={}
	for index,key in enumerate(best_medoids_normal):
		cluster_normal[index]=best_medoids_normal[key]


	# matching clusters from diseased to normal
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
	draw.text((570,660),"For DISEASED",(0,0,255),font=font)
	draw = ImageDraw.Draw(im_normal)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((570,660),"For NORMAL",(0,0,255),font=font)
	im_diseased.show()
	im_normal.show() 
	im_diseased.save("KMEDOID_DISEASED.png")
	im_normal.save("KMEDOID_NORMAL.png") 
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