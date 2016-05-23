library(rjson)
library(MASS)
library(RTextTools)
library(topicmodels)
library(gdata)
library(NLP) 
library(tm)
library(openNLP)
require("NLP")

setwd("/home/abhisheka/Desktop/CN/attachments/DUC01/d05a/ap900322-0200")
getwd()

rm(list=ls(all=TRUE))
fileloc<-"ap900322-0200.txt"
conn <- file(fileloc,open="r")
linn <-readLines(conn)
isIntro=0
txt<-""
for (i in 1:length(linn)) {
  if(linn[i]=="Introduction:"){
    isIntro=1
    next
  }
  if(isIntro==1){
    txt<-paste(txt,linn[i],sep = " ",collapse = NULL)
  }
  
}
txt1<-gsub("[[:space:]]+", " ", txt)
txt1<-gsub("`+", "", txt1)
txt1<-gsub("'+", "", txt1)
txt1<-gsub("[[:space:]]+", " ", txt1)
txt1<-gsub("[@|$|;|:|!|,|_|-|(|)|\"|*|?|{|}]", "", txt1)
txt1<-gsub("[-]", "", txt1)
# sl1<-unlist( strsplit(txt1, "(?<=[^A-Z].[.?]) +(?=[A-Z])", perl = TRUE))
# sl1
sl<-unlist( strsplit(txt1, "(?<=\\.|\\?)\\s(?=[A-Z])", perl = TRUE))
sl

review_source <- VectorSource(txt1)
corpus <- Corpus(review_source)
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
dtm <- as.matrix(DocumentTermMatrix(corpus))
dtm[1,]<-dtm[1,]/rowSums(dtm)

dtm[1,"1700s"]
wordvec<-colnames(dtm)
a<-getscentenceprob(sl[1])
sl[1]
getscentenceprob<-function(sen){
  senlist<-unlist( strsplit(sen," "))
  prob<-0
  for (i in 1:length(senlist)){
    if(senlist[i] %in% wordvec){
      prob<-prob+log(dtm[1,senlist[i]])
    }
  }
  prob
}
b<-seq(1:length(sl))
probvec<-vector(length = length(sl))
names(probvec)<-b

for(i in 1:length(sl)){
  probvec[as.character(i)]<-getscentenceprob(sl[i])
}
probvec<-sort(probvec,decreasing = FALSE)
probvec



log(dtm[1,"mad"])
unlist( strsplit(sl[1]," "))
num=0
## Sumbasic method
for(i in names(probvec)){
  if(num<5){
    print(sl[as.numeric(i)])
    write(sl[as.numeric(i)],file = "ap900322-0200_system.txt",append = TRUE)
    num<-num+1
  }
}
sl

## KL divergence method
library(stringr)
corpus$content
output<-c()
for(i in 1:length(sl)){
  txt1<-gsub(".$", "", sl[i])
  print(txt1)
  unisen<-tolower(unlist( strsplit(txt1, " ", perl = TRUE)))
  uniqueunisen<-unique(unisen)
  coln<-colnames(dtm)
  finterm<-0
  for(j in 1:length(uniqueunisen)){
    if(uniqueunisen[j] %in% coln){
      ##print(uniqueunisen[j])
      q<-(length(grep(uniqueunisen[j], unisen)))/length(unisen)
      finterm<-finterm+dtm[1,uniqueunisen[j]]*log(dtm[1,uniqueunisen[j]]/q)
    }
    ##print(finterm)
  }
  output<-c(output,finterm)
}
names(output)<-b
output
output<-sort(output,decreasing = FALSE)
num<-0
for(i in names(output)){
  if(num<5){
    print(sl[as.numeric(i)])
    write(sl[as.numeric(i)],file = "ap900322-0200_system1.txt",append = TRUE)
    num<-num+1
  }
}

getwd()


unisen<-unlist( strsplit(sl[1], " ", perl = TRUE))
length(grep("Mad", unisen))


dtm[1,"Mad"]



colnames(dtm)
# library(stringi)
# stri_split_boundaries(
#   stri_replace_all_fixed(txt1, "\n", " "),  type="sentence"
# )
# library(openNLPmodels.en)
# library(tm)
# library(stringr)
# library(gsubfn)
# library(plyr)


# scentence<-"I am Abhishek"
# 
# tagPOS <-  function(x, ...) {
#   s <- as.String(x)
#   word_token_annotator <- Maxent_Word_Token_Annotator()
#   a2 <- Annotation(1L, "sentence", 1L, nchar(s))
#   a2 <- annotate(s, word_token_annotator, a2)
#   a3 <- annotate(s, Maxent_POS_Tag_Annotator(), a2)
#   a3w <- a3[a3$type == "word"]
#   POStags <- unlist(lapply(a3w$features, `[[`, "POS"))
#   POStagged <- paste(sprintf("%s/%s", s[a3w], POStags), collapse = " ")
#   list(POStagged = POStagged, POStags = POStags)
# }
# tagPOS(sentence, language = "en", model = NULL, tagdict = NULL)
