#!/usr/bin/env python
import re
import os
import math
import sys
#import simplejson
import __builtin__
from collections import Counter
import pickle


dir1 = "./"
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
	sentence_degree=[]
	for item in sentence_list:
		sentence_degree+=[0]          
	sentence_output.write("--------------------------------------------------------------------------------------------------------------------------------------------")
		#////////////////////////////////till here we selected all sentences in list..................................


	# here we r calculating the degree of sentences in a text 

	
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

	sum=0.0
	for item in sentence_degree:
		sum+=item
	if len(sentence_degree)!=0:
		avg= sum/len(sentence_degree)
	else:
		avg=0
	# calculating the average degree of a text


	#print "Avg degree of sentenes in a document ::  " + str(avg)	
	text_avg+=[round(avg,2)]
	text_count+=1

	#print len(ti)
	c=0
	sl=[]
	sll=[]
	x=0
	
	out_file=file+"_system.txt"
	fi2 = open(os.path.join(dir1, out_file), 'w')
	#fi2=open("out_degree.txt", 'w')

	
	x=0
	m=[]
	sl=[]
	n=[i[0] for i in sorted(enumerate(sen_deg), key=lambda x:x[1], reverse=True)]
	print n
	
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
	
	
	
	# we are calculating the degree of senteces in a summary


	# sum_se = []
	# sum_nw_se = []
	# summary_list=[]
	# text = []
	# sum_sentence_degree=[]

	# fs=open("text-tf.txt",'r').read()
	# fs1=re.sub("[\n]+",' ',fs)

	# sum_se=fs1.split()
	# sum_nw_se= ' '.join(sum_se)

	# summary=re.sub(r'[@|$|;|:|!|,]',r'', sum_nw_se)
	# #print summary
	# #text1=re.sub('[\n]+','',fi)

	# sum_nw_se1= re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', summary)
	# #print sum_nw_se1

	# sv = len(sum_nw_se1)
	# for j in range(0,sv):
	# 	temp=re.sub("\.(?!\d)","",sum_nw_se1[j][:-1])
	# 	summary_list.append(temp)

	# for sitem in summary_list:
	# 	sum_sentence_degree+=[0]
	# #print sentence_list
	# #print"----------------------"
	# #print summary_list




	# dict_sum={}
	# dict_text={}

	# i=0
	# for item in sentence_list:
	# 	dict_text[item]=sentence_degree[i]
	# 	i=i+1
	# #print dict_text

	# #for w,v in dict_text.iteritems():
	# #	if w in summary_list:
	# #		dict_sum[w]=v
	# #		print "100"
	# #print dict_sum

	# for sitem in summary_list:
	# 	    sword=sitem.split(' ')
	# 	    maxi=0
	# 	    for item in sentence_list:
	# 	        word=item.split(' ')
	# 	        count=0;
	# 	        for a in sword:
	# 	            for b in word:
	# 	                if a==b:
	# 	                    count=count +1
	# 	        if(count>maxi):
	# 	            maxi=count
	# 	            dict_sum[sitem] = dict_text[item]
	# #print dict_sum




# 	#print dict_sum
# 	#print "sssssss"
# 	sum_summ=0.0
# 	for item in dict_sum:
# 		sum_summ+=dict_sum[item]
# 	if len(dict_sum)!=0:
# 		savg= sum_summ/len(dict_sum)
# 	else:
# 		savg=0
# 	sum_avg+=[round(savg,3)]
# 	scount+=1
# 		#print "average degree of summary " + str(avg)
# 	#print avg       
# 	#print "111111111111111"

# sentence_output.close()

# #t test analysis.....................................

# sum1=0.0
# sum2=0.0
# print len(sum_avg)
# print len(text_avg)
# for item in sum_avg:
#     sum1+=item
# for item in text_avg:
#     sum2+=item
# sum=0.0
# mean1=sum1/scount
# mean2=sum2/scount
# for item in sum_avg:
#     if scount==1:
#         sum+=0
#     else:
#         sum+=(item-mean1)*(item-mean1)/(scount-1)
# SD1=math.sqrt(sum)
# print "mean value for summary: "+ str(mean1)
# print "mean value for document: "+ str(mean2)
# print "SD for summary:  "+str(SD1)
# sum=0.0
# for item in text_avg:
#     if scount==1:
#         sum+=0
#     else:
#         sum+=(item-mean2)*(item-mean2)/(scount-1)
# SD2=math.sqrt(sum)
# print "SD for document: "+str(SD2)

















