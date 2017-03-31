data_file = open("Lung_carcinoma_ds.csv","r")
mat = []
k,i = 0,0
count=0
for line in data_file.readlines():
	if k==0 or k==1 or k==2 or line.split(',',1)[0]=='NULL':
		k+=1
		continue
	l=[]
	j=0
	count+=1
	for val in line.split(','):
		if j == 0 or j == 1 or j == 2:
			j += 1
			continue
		elif j==98:
		    val = val[:-1]
		    l.append(val)	
		else:
			l.append(val)
		j += 1
	mat.append(l)	
	i += 1
print count


d= open("diseased.txt","a+")
for i in range(0,6672):
	line=""
	for j in range(0,86):
		if j!=85:
			line=line+mat[i][j]+" "
		else:
			line=line+mat[i][j]

	d.write(line)
	d.write("\n")
n=open("normal.txt","a+")	
for i in range(0,6672):
	line=""
	for j in range(0,96):	
		if j<86:
			continue
		elif j!=95:
			line=line+mat[i][j]+" "
		else:
			line=line+mat[i][j]
	n.write(line)
	n.write("\n")	
d.close()
n.close()
data_file.close()


diseased=[]
for i in range(0,6672):
	diseased.append([])
	for j in range(0,86):
		diseased[i].append(mat[i][j])
normal=[]
for i in range(0,6672):
	normal.append([])
	for j in range(0,96):
		if j<86:
			continue
		else:
			normal[i].append(mat[i][j])		

