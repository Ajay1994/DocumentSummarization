#!/usr/bin/env python
import re
import os
import math
import sys
#import simplejson
import __builtin__
from collections import Counter
import pickle


dir1 = "Outputs/sysmix10/"
if not os.path.exists(dir1):
    os.makedirs(dir1)


#th=float(raw_input("enter a threshold: "))
stop_words=[]
fp=open("stop_words.txt","r")
stop_word=fp.readlines()


no_of_stop_words= len(stop_word)
k=0
while k< no_of_stop_words:
	t=stop_word[k][:-2]         #removed \n from sentences
	stop_words.append(t)    
	k=k+1


# read python dict back from the file
pkl_file = open('val_idf.pkl', 'rb')
idf = pickle.load(pkl_file)
pkl_file.close()

#sentence_output=("DUC01_sl.py","w")
#empty list to store avg of text degree and sum degree



text_avg=[]
sum_avg=[]
text_count=0
scount=0

# collecting texts from all directories

sentence_output=open("DUC01_sl.txt","w")
twl=[]

	#  --- collecting text ---
dir_list=os.listdir("DUC01")
for item in dir_list:
    dir_name="DUC01/"+item
    dir_name2="DUC01/"+item
    dir2_list=os.listdir(dir_name)
    for file in dir2_list:
        #result.write("\n"+dir_name+"/"+file)
        file_name=dir_name+"/" +file+"/"+file+".body"
        #sum_name=dir_name2+"/" +file+"/"+file+".abs"
        #print file_name
	#print sum_name

	
	fi=open(file_name,'r').read()
	se = []
	nw_se = []
	sentence_list=[]
	text = []
	fi2=open('input2_test2.text','w')
	
	fi1=re.sub("[\n]+",' ',fi)
	se=fi1.split()

	nw_se= ' '.join(se)
	#print str(nw_se)
	#fi2.write(str(nw_se))	
	#nw_se.replace('"','')
	#nw_se.strip("'")
	#nw_se.strip("''")
	text=re.sub(r'[@|$|;|:|!|,|_|-|(|)|\"|*|?|{|}]',r'', nw_se)
	#nw_sw=re.sub(r'["]',r'', nw_se)
	text=re.sub(r"[''|`|``]",r"", text)
	text=re.sub(r"[-]",r" ", text)
	#var someStr = 'He said "Hello, my name is Foo"';
	#console.log(text.replace(/['"]+/g, ''));
	#text1=re.sub('[\n]+','',fi)
	nw_se1 = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
	#print nw_se1 splitting as per fullstops.
	#fw=open('input2_test22.txt','w')
	v = len(nw_se1)
	for j in range(0,v):
		temp=re.sub("\.(?!\d)","",nw_se1[j])
		sentence_list.append(temp)
	no_of_sentence=len(sentence_list)
	#print sentence_list
	slw=[[] for i in xrange(no_of_sentence)]
	#for l in sentence_list: 
	#	fw.write(str(l)+"\n")
	for i in range(0,len(sentence_list)): 
		word1=sentence_list[i].split()
    		for a in map(str.upper, word1):
        		if a not in map(str.upper, stop_words):
           	 		slw[i].append(a)
				twl.append(a)
				continue
	#sentence_output.write(slw)
	#with open("sentence_output.py", 'w') as file1:
    		#file1.writelines('\t'.join(str(j) for j in i) + '\n' for i in slw)
	for i in range(len(slw)):
		sentence_output.write("[")
		for j in slw[i]:
			sentence_output.write(" %s " % j)
		sentence_output.write("]\n")
	("--------------------------------------------------------------------------------------------------------------------------------------------")
		#////////////////////////////////till here we selected all sentences in list..................................


	# here we r calculating the degree of sentences in a text 

	
	

	mat = [[0 for i in xrange(no_of_sentence)] for i in xrange(no_of_sentence)]
	tf=[]
	tfidf_val={}

	square_ti=0
	sd_tfidf=[]
	test1=[]
	test2=[]
	ti_score=[]
	#print slw
	N=len(slw)
	j=0
	s=0
	for doc in slw:
	#print doc	
		k=0
		for word in doc:
		#print word
		#k=tf_idf(word,doc,slw)
			ktf=doc.count(word)
			kidf=idf[word]
			k=ktf*kidf
			ti_score.append(round(k,3))		





		#test1.append(round(tf_idf(word,doc,slw),2))
			test2.append(round((k*k),3))
		#ti_score += k
			square_ti += k*k
		#print ti_score,square_ti
		tfidf_val[j]=ti_score
		sd_tfidf.append(round(math.sqrt(square_ti),3))
		ti_score=[]
		square_ti=0
		j=j+1
	#print "tfidf values:"
	#print tfidf_val
	#print "sqrd values:"
	#print sd_tfidf
#print len(tfidf_val),no_of_sentence
#print test1
#print test2
	co=0
	for i in xrange(N-1):
		#print word1
		for j in xrange(i+1,N):
			if i==j:
				mat[i][j]=0
			else:
				for word1 in slw[i]:
					for word2 in slw[j]:
			#print word2
						if word1==word2 :
							co=co+1
							in1=slw[i].index(word1)
							in2=slw[j].index(word2)
							cosine= round((tfidf_val[i][in1]*tfidf_val[j][in2])/float(sd_tfidf[i]*sd_tfidf[j]),3)
							#print cosine
							mat[i][j]=cosine
							mat[j][i]=cosine
#	print "lis_matrix"
#	for i in xrange(N):
#		print mat[i]




	#degree
	sen_deg=[]
	for item in sentence_list:
		sen_deg+=[0] 
	th=0.0
	for i in range(no_of_sentence):
		j=i+1
		for j in range(no_of_sentence):
		        sim=mat[i][j]
			#print sim, th
			#print sim>th
			if sim>th:
				#print "true"
		        	sen_deg[i]+=1
				sen_deg[j]+=1
	#print "sentence degree:"	        	
	#print sen_deg
	



	#sentence_strength
	#for i in xrange(N):
#		print mat[i]
	sentence_strength = [[0 for i in xrange(no_of_sentence)] for i in xrange(no_of_sentence)]
	
	for i in range(no_of_sentence):
		j=i+1
		for j in range(no_of_sentence):
			try:
		        	sentence_strength[i][j]=round((1.0/mat[i][j]),3)
			except:
				sentence_strength[i][j]=0

#	print "Sentence strength:"
#	for i in xrange(N):
#		print sentence_strength[i]
	
        #print "degree of sentences in a document ::    "  + str(sentence_degree)
        #print sentence_degree
	ss=[]
	s=0.0
	avg=0.0
	for i in xrange(N):
		s=0
		for j in xrange(N):
			s+=sentence_strength[i][j]
		avg=s/len(sentence_strength[i])
		ss.append(round(avg,3))


	#sP

	sp_matrix = [[0 for i in xrange(no_of_sentence)] for i in xrange(no_of_sentence)]
        for i in range( no_of_sentence):
            for j in range( no_of_sentence):
		sp_matrix[i][j]=100
                for k in range( no_of_sentence):
		    #print mat[i][j]> mat[i][k]+ mat[k][j]
		    #print mat[i][j]
		    sp_matrix[i][j]=float(sentence_strength[i][k]+ sentence_strength[k][j])
                    if (sp_matrix[i][j]> sentence_strength[i][j]):
			sp_matrix[i][j]=float(sentence_strength[i][j])
			#print "ypooooo"
                        #sp_matrix[i][j]=float(mat[i][k]+ mat[k][j])
			#print sp_matrix[i][j]
			#print "out"
		    	#else:
			#sp_matrix[i][j]=float(mat[i][j])
			#print sp_matrix[i][j]
                    
        #print str(count)
	for i in range( no_of_sentence):
            for j in range( no_of_sentence):
		if i==j:
			sp_matrix[i][j]=0.0

#        print "Shortest path mat: "
 #       for i in xrange(N):
#		print sp_matrix[i]

	sp=[]
	
	avg=0.0
	for i in xrange(N):
		s=0.0
		for j in xrange(N):
			s+=sp_matrix[i][j]
		avg=float(s)/len(sp_matrix[i])
		sp.append(round(avg,3))
	#print "avg..........."
	#print sp



	#LIS
	lis_matrix = {}
	
	th=0.02
	for i in range(no_of_sentence):
		j=i+1
		sim=0.0
		l=[]
		for j in range(no_of_sentence):
		        sim=float(mat[i][j])
			#print sim, th
			#print sim>th
			if sim>th:
				#print "true"
		        	sen_deg[i]+=1
				sen_deg[j]+=1
				l.append(j)
		lis_matrix[i]=l
        #print sentence_degree
        #print len(sentence_degree)

	#print lis_matrix
	#print "neighbors lis_matrix"
	#for i in xrange(N):
		#print lis_matrix[i]
	nint=[]
	#print "==============="
	for item in lis_matrix:	
		c=0
		for i in lis_matrix[item]:
			j=i+1
			for j in lis_matrix[item]:
				if j in lis_matrix[i]:
					c+=1
		nint.append(c)
		#print lis_matrix[item]		
		#print item
	
	#print nint
	nl=[]
	next=[]
	for i in range(no_of_sentence):
		if i not in lis_matrix[i]:
			nl.append(i)
	for item in lis_matrix:
		c=0
		for i in lis_matrix[item]:
			for j in nl:
				if j in lis_matrix[i]:
					c+=1
		next.append(c)
	#print next
	s=0
	lis=[]
	for i in range(no_of_sentence):
		try:
			s=float(nint[i])/(nint[i]+next[i])
		except:
			s=0.0		
	#	print s
		lis.append(round(s,3))
		s=0.0
						
	#print lis


	x=0
	m=[]
	sl=[]
	n1=[i[0] for i in sorted(enumerate(sen_deg), key=lambda x:x[1], reverse=True)]
	n2=[i[0] for i in sorted(enumerate(ss), key=lambda x:x[1], reverse=True)]
	n3=[i[0] for i in sorted(enumerate(sp), key=lambda x:x[1], reverse=False)]
	n4=[i[0] for i in sorted(enumerate(lis), key=lambda x:x[1], reverse=True)]
	matrix = [[0 for i in xrange(4)] for i in xrange(no_of_sentence)]
	#print matrix
	#degree
	
	sortedlist1=[]
	for i in range(0,len(n1)):
			sortedlist1.append(n1[i])
	
	#strength
	sortedlist2=[]
	for i in range(0,len(n2)):
			sortedlist2.append(n2[i])
			

	#sp
	sortedlist3=[]
	for i in range(0,len(n3)):
			sortedlist3.append(n3[i])
			

	#lis
	sortedlist4=[]
	for i in range(0,len(n4)):
			sortedlist4.append(n4[i])
		
	
	for i in range(no_of_sentence):
		j=0
		matrix[i][j]=0.5+sortedlist1.index(i)
		j=j+1
		matrix[i][j]=0.25+sortedlist2.index(i)
		j=j+1
		matrix[i][j]=1.5+sortedlist3.index(i)
		j=j+1
		matrix[i][j]=0.25+sortedlist4.index(i)		

  
	print "---------------------------------------"   
	print matrix
	
	imatrix = []
	
	#inverse method
	for i in range(no_of_sentence):
		s=0
		for j in range(4):
			try:
				s+=(1.0/matrix[i][j])
		
			except:
				pass

		imatrix.append(round(s,3))
	

	print "========================================="
	print imatrix


	out_file=file+"_system.txt"
	fi2 = open(os.path.join(dir1, out_file), 'w')

	n=[i[0] for i in sorted(enumerate(imatrix), key=lambda x:x[1], reverse=True)]
	sortedlist=[]
	j=0
	for i in range(0,len(n)):
			sortedlist.append(n[i])
			j=j+1
			if j==5:			
				break
		
	#sortedlist.sort()
	
	print file 
	print sortedlist
	c=0
	for i in range(0,len(sortedlist)):
    		x=sortedlist[i]
			
		s=str(sentence_list[x])
		#print s
		p1 = re.compile(r'<P>|</P>')
		m1=filter(None, p1.split(s))
		print m1
		l=[]
		for j in m1:
			if c<100:
				p11 = re.compile(r' ')
				m11=filter(None, p11.split(j))
				#print m11
				c+=len(m11)
				#fi2.write(".\n")			
				fi2.write(j+".\n")
				print "done"	
	print ""
			#fi2.write(j+".\n")
				
				
    			#x=0
    			#fi2.write(".\n")
   
	
	fi2.close()


		

