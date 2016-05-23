'''  Verification of hypothesis based on LIS of sentences..... calculation ......................
Algorithm:

'''
#!/usr/bin/env python
import re
import os
import math
import sys
#import simplejson
import __builtin__
from collections import Counter
import pickle

dir1 = "Outputs/systemlis/"
if not os.path.exists(dir1):
    os.makedirs(dir1)

pkl_file = open('val_idf.pkl', 'rb')
idf = pickle.load(pkl_file)
pkl_file.close()

fp=open("stop_words.txt","r")
stop_words=fp.readlines()
no_of_stop_words= len(stop_words)
i=0
k=0
count1=0
count2=0
sum_avg=[]
while k< no_of_stop_words:
	t=stop_words[k][:-2]         #removed \n from sentences
	stop_words.append(t)    
	k=k+1
#print stop_words


document_list=[]
summary_list=[]
count1=0
count2=0
# till here I calculated stop words
dir_list=os.listdir("DUC01")
for item in dir_list:
    dir_name="DUC01/"+item
    dir_name2="DUC01/"+item
    dir2_list=os.listdir(dir_name)
    for file in dir2_list:
        #result.write("\n"+dir_name+"/"+file)
        file_name=dir_name+"/" +file+"/"+file+".body"
        sum_name=dir_name2+"/" +file+"/"+file+".abs"
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
				
				continue
        #print sentence_list

        sentence_degree=[]
        for item in sentence_list:
            sentence_degree+=[0]           #because i later i also matched a sentence with itself
	no_of_sentence=len(sentence_list)

        #////////////////////////////////till here we selected all sentences in list..................................
	sen_deg=[]
	for item in sentence_list:
		sen_deg+=[0] 


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
	print "matrix"
	for i in xrange(N):
		print mat[i]

	matrix = {}
	
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
		matrix[i]=l
        #print sentence_degree
        #print len(sentence_degree)

	print matrix
	#print "neighbors matrix"
	#for i in xrange(N):
		#print matrix[i]
	nint=[]
	print "==============="
	for item in matrix:	
		c=0
		for i in matrix[item]:
			j=i+1
			for j in matrix[item]:
				if j in matrix[i]:
					c+=1
		nint.append(c)
		#print matrix[item]		
		#print item
	
	print nint
	nl=[]
	next=[]
	for i in range(no_of_sentence):
		if i not in matrix[i]:
			nl.append(i)
	for item in matrix:
		c=0
		for i in matrix[item]:
			for j in nl:
				if j in matrix[i]:
					c+=1
		next.append(c)
	print next
	s=0
	val=[]
	for i in range(no_of_sentence):
		try:
			s=float(nint[i])/(nint[i]+next[i])
		except:
			s=0.0		
		print s
		val.append(round(s,3))
		s=0.0
						


	print val
        


        #print "degree of sentences in a document ::    "  + str(sentence_degree)
        #print sentence_degree
        
	c=0
	sl=[]
	sll=[]
	x=0
	
	out_file=file+"_system.txt"
	fi2 = open(os.path.join(dir1, out_file), 'w')
	#fi2=open("out_LIS.txt", 'w')

	
	x=0
	m=[]
	sl=[]
	n=[i[0] for i in sorted(enumerate(val), key=lambda x:x[1], reverse=True)]
	print n
	start=0
	end=5
	sortedlist1=[]
	j=0
	for i in range(0,len(n)):
		sortedlist1.append(n[i])
		j=j+1
		if j==5:
			break		
		
		
	sortedlist1.sort()
	print sortedlist1
	for i in range(0,len(sortedlist1)):
    		x=sortedlist1[i]
			
		s=str(sentence_list[x])
			#print s
		p1 = re.compile(r'<P>|</P>')
		m1=filter(None, p1.split(s))
			#print m1
		l=[]
		for j in m1:
			if c<100:
				p11 = re.compile(r' ')
				m11=filter(None, p11.split(j))
				#print m11
				c+=len(m11)
				#fi2.write(".\n")			
				fi2.write(j+".\n")
				break
			
			#fi2.write(j+".\n")
				
				
    			#x=0
    			#fi2.write(".\n")
   
	
	fi2.close()
	
        #///////////////////////////// till here we calculated the avg degree of document sentences .................................

#         sum_se = []
# 	sum_nw_se = []
# 	summary_list=[]
# 	text = []
# 	sum_sentence_degree=[]

# 	fs=open(sum_name,'r').read()
# 	fs1=re.sub("[\n]+",' ',fs)

# 	sum_se=fs1.split()
# 	sum_nw_se= ' '.join(sum_se)

# 	summary=re.sub(r'[@|$|;|:|!|,]',r'', sum_nw_se)
# 	#print summary
# 	#text1=re.sub('[\n]+','',fi)

# 	sum_nw_se1= re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', summary)
# 	#print sum_nw_se1

# 	sv = len(sum_nw_se1)
# 	for j in range(0,sv):
# 		temp=re.sub("\.(?!\d)","",sum_nw_se1[j][:-1])
# 		summary_list.append(temp)                     #summary list.......................................................
#         #print sentence_list1
#         #print sentence_list[0][0:-2]
#         no_of_sentence1= len(sentence_list)
#         i=0
#         while i< no_of_sentence1:
#             sentence_list[i]=sentence_list[i][0:-2]         #removed . and \n from sentences
#             i=i+1
#         #print sentence_list1
#         dict_text={}
# 	i=0
# 	for item in sentence_list:
# 		dict_text[item]=sentence_degree[i]
# 		i=i+1
	

#         #print dict_text
#         dict_sum={}
#         #for item in sentence_list:
#           #  dict2[item]=0
#           #  i=i+1

#         for sitem in summary_list:
# 		    sword=sitem.split(' ')
# 		    max=0
# 		    for item in sentence_list:
# 		        word=item.split(' ')
# 		        count=0;
# 		        for a in sword:
# 		            for b in word:
# 		                if a==b:
# 		                    count=count +1
# 		        if(count>max):
# 		            max=count
#                     	    dict_sum[sitem] = dict_text[item]

#         #print dict1
#         #print "summary.................."
#         #print dict2
#         sum_summ=0.0
# 	savg=0
# 	for item in dict_sum:
# 		sum_summ+=dict_sum[item]
# 	if len(dict_sum)!=0:
# 		savg= sum_summ/len(dict_sum)
# 	else:
# 		savg=0
# 	sum_avg+=[round(savg,3)]
#         count2+=1
#         #print "average degree of summary " + str(avg)
#         #result.write("   "+str(round(avg,2)))
        
	
    
# print "terminate"

# #test analysis.....................................
# import math

