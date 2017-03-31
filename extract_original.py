data_file = open("gene_result.txt","r")
gene = []
k=0
for line in data_file.readlines():
	if k==0:
		k=k+1
		continue
	val=line.split("\t",6)[5]
	gene.append(val)	
from Gene_vs_DataPoints import Corresponding_Gene
gene_name=[]
for i in range(0,6672):
	gene_name.append(Corresponding_Gene[i])
gene=list(set(gene_name) & set(gene))

print len(gene)

name_of_gene = open('gene_names_updated.txt','w+')
counter = 1
global_counter = 1

for name in gene:
	if global_counter > 713:
		break
	if (counter % 9 ) == 0:
		name_of_gene.write('\n')
		n_string = name.ljust(len(name)+2,' ')
		name_of_gene.write(n_string)
		counter = 2
		global_counter += 1
	else:
		n_string = name.ljust(len(name)+2,' ')
		name_of_gene.write(n_string)
		counter += 1
		global_counter += 1

print "done"



