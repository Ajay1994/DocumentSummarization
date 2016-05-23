
## @auther -> Krunal Parmar
# include library for nlp function.
library(NLP) 
library(openNLP)
library(tm)

# function for getting pos tags frm sentence.
tagPOS <-  function(x, ...) {
  s <- as.String(x)
  word_token_annotator <- Maxent_Word_Token_Annotator()
  a2 <- Annotation(1L, "sentence", 1L, nchar(s))
  a2 <- annotate(s, word_token_annotator, a2)
  a3 <- annotate(s, Maxent_POS_Tag_Annotator(), a2)
  a3w <- a3[a3$type == "word"]
  POStags <- unlist(lapply(a3w$features, `[[`, "POS"))
  POStagged <- paste(sprintf("%s/%s", s[a3w], POStags), collapse = " ")
  POStagged
}

# set working directory to parent of DUC01 directory.
# make one directory named summary for generate summaries in that folder
setwd("F:/kgp working/cn proj")

# getting all the filesin duc01 recursively.
files <- list.files(path = "./DUC01/", pattern = NULL, all.files = FALSE,
                    full.names = FALSE, recursive = T,
                    ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)

# vector which stores text file names
textFiles <- c()

# vector to store all weights to plot the graph
allweights <- c()

# making list of all txt files
for(i in 1: length(files)){
  if(grepl(".txt", files[i])){
    textFiles <- c(textFiles, files[i])
  }
}

# directory of dataset
baseaddr <- "F:/kgp working/cn proj/DUC01/"

## for each document , do..
for(textFile in textFiles){
  ## constructing o/p file name 
  filename <- unlist(strsplit(textFile,split = "/"))
  filename <- filename[3]
  outputFile <- substr(filename,1,nchar(filename)-4) 
  outputFile <- paste("./summary/", outputFile,"_system.txt", sep = "")
  
  paste(baseaddr,textFile,sep = "")
  ## reading text file
  myfilecontent <-  readLines(paste(baseaddr,textFile,sep = ""))
  myfilecontent <- myfilecontent[-1]
  
  txt <- paste(myfilecontent,collapse = " ")
  
  ## tokenizing and cleaning 
  txt1<-gsub("[[:space:]]+", " ", txt)
  txt1<-gsub("`+", "", txt1)
  txt1<-gsub("'+", "", txt1)
  txt1<-gsub("[[:space:]]+", " ", txt1)
  txt1<-gsub("[@|$|;|:|!|,|_|-|(|)|\"|*|?|{|}]", "", txt1)
  txt1<-gsub("[-]", "", txt1)
  sentences<-unlist( strsplit(txt1, "(?<=[^A-Z].[.?]) +(?=[A-Z])", perl = TRUE))
  
  ## take sentence and do pos tag
  sentences <- paste(sentences,collapse = "%")
  taggedSentence <- tagPOS(sentences)
  sentences <- unlist(strsplit(x = taggedSentence,split = "%"))
  
  ## assign the weight to each word and avg. it for weight of whole sentence
  
  # store weight of  each sentence 
  weightOfSentence <- c()
  
  for(sentence in sentences){
    words <- unlist(strsplit(x = sentence,split = " "))
    impwords <- c()
    withoutstopwords <- c()
    for(word in words){
      checkTag <- unlist(strsplit(word,"/"))
      withoutstopwords <- c(withoutstopwords,checkTag[1])
      if(!is.na(checkTag[2]) && !is.na(checkTag[1])){
        if(as.character(checkTag[2]) == "NN" || as.character(substr(checkTag[2],0,2)) == "VB" || as.character(checkTag[2]) == "JJ" || as.character(checkTag[2]) == "CD" ){
          impwords <- c(impwords,checkTag[1])
        }
      }
    }
    ## count words without stop words for normalization.
    withoutstopwords <- paste(withoutstopwords,collapse = " ")
    j <- Corpus(VectorSource(withoutstopwords))
    jj <- tm_map(j, removeWords, stopwords('english'))
    withoutstopwords <- jj[[1]]$content
    withoutstopwords <- unlist(strsplit(withoutstopwords,split = " "))
    freqWord <- as.list(table(impwords))
    
    
    ## find p(wi)
    probWords <- lapply(freqWord,function(x) x/(length(withoutstopwords)))
    
    weightOfSentence <- c(weightOfSentence,sum(unlist(probWords)))
    allweights <- c(allweights,weightOfSentence)
  }
  
  names(weightOfSentence) <- 1:length(weightOfSentence)
  sortedByWeights <- names(sort(weightOfSentence,decreasing = T))
  i <- 1
  result <-c()
  while(i<6){
    result <- c(result,sentences[as.numeric(sortedByWeights[i])])
    i <- i+1
  }
  
  ## find summary till 100 words.
  noOFWords <- 0
  resultsen <- c()
  for(res in result) {
    sen <- unlist(strsplit(res,split = " "))
    for(word in sen){
      senwords <-unlist(strsplit(x = word,split = "/"))
      resultsen <- c(resultsen,senwords[1])
      noOFWords <- noOFWords + 1
      if(noOFWords == 100){
        break;
      }
    }
  }
  finalSummary <- paste(resultsen,collapse = " ")
  finalSummary <- gsub(" , ", ",", as.String(finalSummary))
  finalSummary <- gsub(" . ", ". ", as.String(finalSummary))
  ## write summary in o/p file
  write(finalSummary, outputFile)
}
