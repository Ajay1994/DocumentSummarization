'''  Verification of hypothesis based on strength of sentences .....calculation ......................
Algorithm:
step1. read all the sentences from original documents
step2. compare one sentence to another and count the no of words which are matched
step3. if count> threshold value then we assumed that sentences are similar
step4. add weight of the edge in sentences
step5. read all the sentences from summary and calculate the strength of sentences from original graph
step6. print the average strength of all sentences in documents and average strength of sentences of summary

'''
import re
import os
import math
import sys
#import simplejson
import __builtin__
from collections import Counter
import pickle


dir1 = "Outputs/systemsp/"
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

#print stop_words
count1=0
count2=0
document_list=[]
summary_list=[]
sum_avg=[]



# collecting texts from all directories
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
	#sentence_output.write(slw)
	#with open("sentence_output.py", 'w') as file1:
    		#file1.writelines('\t'.join(str(j) for j in i) + '\n' for i in slw)
	
        sentence_strength=[]
        for item in sentence_list:
            sentence_strength+=[0]           #because i later i also matched a sentence with itself


        #////////////////////////////////till here we selected all sentences in list..................................

	
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
			test2.append(round((k*k),2))
		#ti_score += k
			square_ti += k*k
		#print ti_score,square_ti
		tfidf_val[j]=ti_score
		sd_tfidf.append(round(math.sqrt(square_ti),3))
		ti_score=[]
		square_ti=0
		j=j+1
#print test1
	print "tf-idf values...."
	print tfidf_val
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
	#print co
	print "cosine similarity matrix:"
	for i in xrange(N):
		print mat[i]


	sen_st = [[0 for i in xrange(no_of_sentence)] for i in xrange(no_of_sentence)]
	
	for i in range(no_of_sentence):
		j=i+1
		for j in range(no_of_sentence):
			try:
		        	sen_st[i][j]=round((1.0/mat[i][j]),3)
			except:
				sen_st[i][j]=0

	print "Sentence strength:"
	for i in xrange(N):
		print sen_st[i]
        #print sen_str
        #print "original matrix"
        #print matrix
        matrix = [[0 for i in xrange(no_of_sentence)] for i in xrange(no_of_sentence)]
        for i in range( no_of_sentence):
            for j in range( no_of_sentence):
		matrix[i][j]=100
                for k in range( no_of_sentence):
		    #print mat[i][j]> mat[i][k]+ mat[k][j]
		    #print mat[i][j]
		    matrix[i][j]=float(sen_st[i][k]+ sen_st[k][j])
                    if (matrix[i][j]> sen_st[i][j]):
			matrix[i][j]=float(sen_st[i][j])
			#print "ypooooo"
                        #matrix[i][j]=float(mat[i][k]+ mat[k][j])
			#print matrix[i][j]
		#print "out"
		    #else:
			#matrix[i][j]=float(mat[i][j])
			#print matrix[i][j]
                    
        #print str(count)
	for i in range( no_of_sentence):
            for j in range( no_of_sentence):
		if i==j:
			matrix[i][j]=0.0

        print "Shortest path mat: "
        for i in xrange(N):
		print matrix[i]

       	
	ss=[]
	
	avg=0.0
	for i in xrange(N):
		s=0.0
		for j in xrange(N):
			s+=matrix[i][j]
		avg=float(s)/len(matrix[i])
		ss.append(round(avg,3))
	print "avg..........."
	print ss

        
        #print sen_str
        
        #print "ST"
        #print sen_str
        #print len(sen_str)
        #print "degree of sentences in a document ::    "  + str(sentence_degree)
        #print sentence_degree
        sum=0.0
        for item in ss:
            sum+=item
        #print sum
        if len(ss)!=0:
            avg= sum/len(ss)
        else:
            avg=0
        #print avg
        #print "Avg strength of sentenes in a document ::  " + str(avg)
        #avg=avg+rand
        #result.write("     "+str(round(avg,2)))
        document_list+=[round(avg,2)]
        count1+=1
        

	out_file=file+"_system.txt"
	fi2 = open(os.path.join(dir1, out_file), 'w')
	#fi2=open("out_degree.txt", 'w')

	c=0
	sl=[]
	sll=[]
	x=0
	m=[]
	sl=[]
	n=[i[0] for i in sorted(enumerate(ss), key=lambda x:x[1])]
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
	
        #///////////////////////////// till here we calculated the avg degree of document sentences .................................

#       	sum_se = []
# 	sum_nw_se = []
# 	summary_list=[]
# 	text = []
# 	sum_sentence_degree=[]

# 	fs=open("text-tf.txt",'r').read()
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
# 		temp=re.sub("\.(?!\d)","",sum_nw_se1[j])
# 		summary_list.append(temp)
#         #print sentence_list1
        
#         dict_sum={}
# 	dict_text={}
#         i=0

        
# 	for item in sentence_list:
# 		dict_text[item]=sentence_strength[i]
# 		i=i+1

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
# 		            dict_sum[sitem] = dict_text[item]
#         #print dict1
#         sum_summ=0.0
	
# 	for item in dict_sum:
# 		sum_summ+=dict_sum[item]
# 	if len(dict_sum)!=0:
# 		savg= sum_summ/len(dict_sum)
# 	else:
# 		savg=0
# 	sum_avg+=[round(savg,3)]
#         count2+=1
#         #print "average strength of summary " + str(avg)
#         #avg+=rand
#         #result.write("           " + str(round(avg,2)))
#         #summary_list+=[round(avg,2)]
#         #count2+=1
      	
# print "terminated"

# #t test analysis.....................................
# import math
# print len(sum_avg)
# print len(document_list)
# sum1=0.0
# sum2=0.0
# print str(count1)
# print str(count2)
# for item in sum_avg:
#     sum1+=item
# for item in document_list:
#     sum2+=item
# sum=0.0
# mean1=sum1/count1
# mean2=sum2/count2
# for item in sum_avg:
#     sum+=(item-mean1)*(item-mean1)/(count1-1)
# SD1=math.sqrt(sum)
# print "mean value for summary"+ str(mean1)
# print "mean value for document"+ str(mean2)
# print "SD for summary:  "+str(SD1)
# sum=0.0
# for item in document_list:
#     sum+=(item-mean2)*(item-mean2)/(count1-1)
# SD2=math.sqrt(sum)
# print "SD for document: "+str(SD2)

