library(rjson)
library(MASS)
library(RTextTools)
library(topicmodels)
library(gdata)
library(NLP) 
library(tm)
library(openNLP)
require("NLP")


####set the directory to where the texts of the articles has been kept
setwd("/home/abhisheka/Desktop/Source")
getwd()
rm(list=ls(all=TRUE))

files <- list.files(path = "./", pattern = "*.txt", all.files = FALSE,
                    full.names = FALSE, recursive = T,
                    ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
substr(files[1],1,nchar(files[1])-4)

fileloc<-files[1]

for(k in 1:length(files)){
    fileloc<-files[k]
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
    setwd("/home/abhisheka/Desktop/summary")
    txt1<-gsub("[[:space:]]+", " ", txt)
    txt1<-gsub("`+", "", txt1)
    txt1<-gsub("'+", "", txt1)
    txt1<-gsub("[[:space:]]+", " ", txt1)
    txt1<-gsub("[@|$|;|:|!|,|_|-|(|)|\"|*|?|{|}]", "", txt1)
    txt1<-gsub("[-]", "", txt1)
    sl1<-unlist( strsplit(txt1, "(?<=[^A-Z].[.?]) +(?=[A-Z])", perl = TRUE))
    sl1
    # sl<-unlist( strsplit(txt1, "(?<=\\.|\\?)\\s(?=[A-Z])", perl = TRUE))
    # sl
    
    review_source <- VectorSource(txt1)
    corpus <- Corpus(review_source)
    corpus <- tm_map(corpus, content_transformer(tolower))
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, stripWhitespace)
    corpus <- tm_map(corpus, removeWords, stopwords("english"))
    dtm <- as.matrix(DocumentTermMatrix(corpus))
    dtm[1,]<-dtm[1,]/rowSums(dtm)
    wordvec<-colnames(dtm)
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
    b<-seq(1:length(sl1))
    probvec<-vector(length = length(sl1))
    names(probvec)<-b
    
    for(i in 1:length(sl1)){
      probvec[as.character(i)]<-getscentenceprob(sl1[i])
    }
    probvec<-sort(probvec,decreasing = FALSE)
    probvec
    
    
    # 
    # log(dtm[1,"mad"])
    # unlist( strsplit(sl[1]," "))
    num=0
    
    ## Sumbasic method
    for(i in names(probvec)){
      if(num<5){
        print(sl1[as.numeric(i)])
        # write(sl1[as.numeric(i)],file = "ap900322-0200_system.txt",append = TRUE)
        num<-num+1
      }
    }
    
    ## KL divergence method
    library(stringr)
    corpus$content
    output<-c()
    for(i in 1:length(sl1)){
      txt1<-gsub(".$", "", sl1[i])
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
    outputfile<-paste(trim(substr(fileloc,1,nchar(fileloc)-4)),"_system.txt",collapse = "")
    outputfile<-gsub(" ", "", outputfile) 
    print(outputfile)
    num<-0
    summaryVector<-c()
    for(i in names(output)){
      if(num<7){
        print(sl1[as.numeric(i)])
        sent<-unlist( strsplit(sl1[as.numeric(i)], " ", perl = TRUE))
        for(word in sent){
          summaryVector <- c(summaryVector,word)
          if(length(summaryVector) == 100){
            break;
          }
          }
          if(length(summaryVector) == 100){
            break;
          }
        }
        num<-num+1
      }
     summaryVector <- paste(summaryVector,collapse = " ")
     write(summaryVector,file = outputfile,append = TRUE)
    setwd("/home/abhisheka/Desktop/Source")
}

length(unlist(strsplit(sl1[1]," ",perl = TRUE)))
getwd()


unisen<-unlist( strsplit(sl1[1], " ", perl = TRUE))
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
