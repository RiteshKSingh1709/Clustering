import numpy as np
import math
from util1 import calculate_cost,proposed,importdata
import sys
from PIL import Image, ImageDraw,ImageFont
from extract_original import gene
from Gene_vs_DataPoints import Corresponding_Gene

def main():
	k=int(raw_input("Enter the no of clusters:"))
	e=int(raw_input("Enter the no of iterations:"))
	data=importdata("./diseased.txt")
	mincost=float('inf')
	best_cls,best_cluster=proposed(data,k,e)
	print best_cluster
	cluster_diseased = {0:[],1:[],2:[]}	
	j=0
	for i in best_cls:
	    if i==0:
	        cluster_diseased[i].append(j)
	    if i==1:
	        cluster_diseased[i].append(j)
	    if i==2:
	        cluster_diseased[i].append(j)
	    j=j+1
	for j,i in enumerate(cluster_diseased):
		cluster_diseased[i].append(best_cluster[i])
		print i,":",len(cluster_diseased[i])
	e=int(raw_input("Enter the no of iterations:"))
	data=importdata("./normal.txt")
	mincost=float('inf')
	best_cls,best_cluster=proposed(data,k,e)
	print best_cluster
	cluster_normal = {0:[],1:[],2:[]}	
	j=0
	for i in best_cls:
	    if i==0:
	        cluster_normal[i].append(j)
	    if i==1:
	        cluster_normal[i].append(j)
	    if i==2:
	        cluster_normal[i].append(j)
	    j=j+1

	for j,i in enumerate(cluster_normal):
		cluster_normal[i].append(best_cluster[i])
		print i,":",len(cluster_normal[i])  
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






















