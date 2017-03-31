import Tkinter as tk
import tkFileDialog
import tkFont
import os
import subprocess

no_cluster = 0

def proposed_frame(name):
	global top,no_cluster
	# top.destroy()
	master = tk.Tk()
	customFont = tkFont.Font(family="Helvetica", size=12)
	tk.Label(master,text="B-CLARANS ALGORITHM",fg="blue",padx=5,pady=5,font=customFont)
	no_cluster = tk.StringVar()
	file_opt = options = {}
	options['defaultextension'] = '.txt'
	options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
	options['initialdir'] = 'C:\\'
	options['initialfile'] = 'myfile.txt'
	# options['parent'] = root
	options['title'] = 'This is a title'

	tk.Label(master,text="Enter the filepath :").grid(row=1,column=0)
	tkFileDialog.askopenfilename(**file_opt)
	#labels and textBoxes
	tk.Label(master,text="Enter the number of cluster:").grid(row=0,column=0)
	tk.Entry(master,textvariable = no_cluster).grid(row=0,column=1)


	tk.Button(master,text = "Quit" ,fg="black",bg="red", command = master.quit,width=25).grid(row=5,column=0)
	tk.Button(master,text = "Run",fg="black",bg="green",command = lambda : Run(name,no_cluster),width=25).grid(row=5,column=1)

def special_frame(name):
    global top,no_cluster
    # top.destroy()
    master = tk.Tk()
    customFont = tkFont.Font(family="Helvetica", size=12)
    tk.Label(master,text="FUZZY C-MEANS ALGORTIHM",fg="blue",padx=5,pady=5,font=customFont)
    no_cluster = tk.StringVar()
    dimension = tk.StringVar()
    fuzziness = tk.StringVar()
    ter_criteria = tk.StringVar()
    dimension_for_diseased = tk.StringVar()
    dimension_for_normal = tk.StringVar()

    #lables and textboxes
    tk.Label(master,text="Enter the number of cluster:").grid(row=0,column=0)
    tk.Entry(master,textvariable = no_cluster).grid(row=0,column=1)

    tk.Label(master,text="Enter the number of datapoints:").grid(row=1,column=0)
    tk.Entry(master,textvariable = dimension).grid(row=1,column=1)

    tk.Label(master,text="Enter the fuzziness").grid(row=2,column=0)
    tk.Entry(master,textvariable= fuzziness).grid(row=2,column=1)

    tk.Label(master,text ="Enter the termination criteria").grid(row=3,column=0)
    tk.Entry(master,textvariable = dimension_for_diseased).grid(row=3,column=1)

    tk.Label(master,text = "Enter the dimension for normal").grid(row = 4,column=0)
    tk.Entry(master,textvariable = dimension_for_normal).grid(row=4,column=1)

    #buttons added here 

    tk.Button(master,text = "Quit" ,fg="black",bg="red", command = master.quit,width=25).grid(row=5,column=0)
    tk.Button(master,text = "Run",fg="black",bg="green",command = lambda : Run(name,no_cluster),width=25).grid(row=5,column=1)

def generic_frame(name):
	global top
	top.destroy()
	global no_cluster
	print "here"
	master = tk.Tk()
	
	no_cluster = tk.StringVar()

	#lables and textbox registered here ...!!
	tk.Label(master, text="Enter number of cluster yu want..!!").grid(row=0)
	tk.Entry(master,textvariable=no_cluster).grid(row=0,column=1)
	#no_cluster.set(int(no_cluster.get()))
	print no_cluster , " printed it ..!!"
	
	#Buttons registered here ...
	tk.Button(master, text='Quit', bg="red",fg="black",command=master.quit,width=10).grid(row=3, column=0, pady=4)
	tk.Button(master, text='Run', bg="green",fg="black",command=lambda:Run(name,no_cluster.get()),width=10).grid(row=3, column=1, pady=4)
	#here we will use no_cluster.get()
	#l1.pack();b1.pack();b2.pack();

def Run(name,no_cluster):
	print os.getcwd()
	# for fuzzy c-means we have to handle it differntly ..!! 
	print os.getcwd(),"here i come till here everything is ok",int(no_cluster)
	pckg_name = name + '.main'
	print pckg_name , "printed the package name "
	
	#package is called here using subprocess ...!!
	if 'FCM' in pckg_name.split('.')[0]:
	    subprocess.call()
	else:
            subprocess.call(['python','-m',pckg_name,no_cluster])	
	print "over to tkinter"



top = tk.Tk()
customFont = tkFont.Font(family="Helvetica", size=12)
tk.Label(top,text="Different Clustering Algorithms implemented in Python",fg="blue",padx=5,pady=5,font=customFont).pack(padx=10,pady=10)
w = tk.Button(top,text="AGGLOMERATIVE",padx=10,pady=10,command=lambda :generic_frame("AGGLOMERATIVE"),width=25)
w1 = tk.Button(top,text="FCM",padx=10,pady=10,command=lambda :special_frame("FCM"),width=25)
w2 = tk.Button(top,text="CLARANS",padx=10,pady=10,command=lambda : generic_frame("CLARANS"),width=25)
w3 = tk.Button(top,text="KMEANS",padx=10,pady=10,command=lambda :generic_frame("KMEANS"),width=25)
w4 = tk.Button(top,text="KMEDOIDS",padx=10,pady=10,command=lambda :generic_frame("KMEDOIDS"),width=25)
w5 = tk.Button(top,text="X-CLARANS",padx=10,pady=10,command=lambda :proposed_frame("X-CLARANS"),width=25)
w6 = tk.Button(top,text="B-CLARANS",padx=10,pady=10,command=lambda :proposed_frame("B-CLARANS"),width=25)
w.pack(pady=10) ; w1.pack(pady=10); w2.pack(pady=10) ; w3.pack(pady=10) ; w4.pack(pady=10);w5.pack(pady=10);w6.pack(pady=10);
top.mainloop()
