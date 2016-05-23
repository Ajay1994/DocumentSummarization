##############################################
setwd("E:/IIT KHARAGPUR/Semester II/Complex Networks/Project/workspace")
files <- list.files(path = "./DUC01/", pattern = NULL, all.files = FALSE,
                    full.names = FALSE, recursive = T,
                    ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
textFiles <- c()
for(i in 1: length(files)){
  if(grepl(".txt", files[i])){
    textFiles <- c(textFiles, files[i])
  }
}
for(i in 1: length(textFiles)){
  fileloc <- paste("./DUC01/", textFiles[i], sep = "")
  filename <- unlist(strsplit(fileloc, split = "/"))
  outputFile <- filename[5]
  outputFile <- substr(outputFile,1,nchar(outputFile)-4) 
  outputFile <- paste("./summary/", outputFile,"_system.txt", sep = "")
  
  linn <-readLines(fileloc)
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
  sentences<-unlist( strsplit(txt1, "(?<=[^A-Z].[.?]) +(?=[A-Z])", perl = TRUE))
  
  if(length(sentences) < 7){
    write(sentences, outputFile)
  }else{
    ##############################################
    #Tf- Idf Calculation
    
    corpusText <- VectorSource(sentences)
    corpusText <- Corpus(corpusText)
    corpus <- tm_map(corpusText, content_transformer(tolower))
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, stripWhitespace)
    corpus <- tm_map(corpus, removeWords, stopwords("english"))
    terms <- TermDocumentMatrix(corpus,control = list(wordLengths=c(1,Inf), weighting=weightTfIdf))
    #tfidf <- as.matrix(terms)
    
    removeSparseTerms(terms, sparse=0.90)
    tfidf <- as.matrix(terms)
    tfidf <- t(tfidf)
    distMatrix <- dist(scale(tfidf))
    d <- as.matrix(distMatrix)
    
    
    fit <- hclust(distMatrix, method = "ward.D") 
    plot(fit) # display dendogram
    groups <- cutree(fit, k=4) # cut tree into 5 clusters
    # draw dendogram with red borders around the 5 clusters 
    rect.hclust(fit, k=4, border="red")
    
    ##################################################
    cluster <- which(groups == 1)
    cluster1 <- names(cluster)
    cluster1Sentences <- c()
    for(i in 1: length(cluster1)){
      cluster1Sentences <- c(cluster1Sentences, sentences[as.integer(cluster1[i])])
    }
    
    cluster <- which(groups == 2)
    cluster2 <- names(cluster)
    cluster2Sentences <- c()
    for(i in 1: length(cluster2)){
      cluster2Sentences <- c(cluster2Sentences, sentences[as.integer(cluster2[i])])
    }
    
    cluster <- which(groups == 3)
    cluster3 <- names(cluster)
    cluster3Sentences <- c()
    for(i in 1: length(cluster3)){
      cluster3Sentences <- c(cluster3Sentences, sentences[as.integer(cluster3[i])])
    }
    
    cluster <- which(groups == 4)
    cluster4 <- names(cluster)
    cluster4Sentences <- c()
    for(i in 1: length(cluster4)){
      cluster4Sentences <- c(cluster4Sentences, sentences[as.integer(cluster4[i])])
    }
    
    
    ####################################################
    #Re run of clustering algorithm
    
    getSortedRankedSentences <- function(clusterSentences){
      # print(clusterSentences)
      if(length(clusterSentences) > 1){
        print("inif")
        corpusText1 <- VectorSource(clusterSentences)
        corpusText1 <- Corpus(corpusText1)
        corpus1 <- tm_map(corpusText1, content_transformer(tolower))
        corpus1 <- tm_map(corpus1, removePunctuation)
        corpus1 <- tm_map(corpus1, stripWhitespace)
        corpus1 <- tm_map(corpus1, removeWords, stopwords("english"))
        terms1 <- DocumentTermMatrix(corpus1,control = list(wordLengths=c(1,Inf), weighting=weightTfIdf))
        tfidf1 <- as.matrix(terms1)
        
        d1 <- dist(as.matrix(tfidf1))
        temp1 <- as.matrix(d1)
        
        eigenValues <- eigen(temp1)
        #eigenValues$values
        eigenvectors <- as.matrix(eigenValues$vectors)
        principalVector <- eigenvectors[,1]
        names(principalVector) <- seq(1:length(principalVector))
        sortedprincipalVector <- sort(principalVector, decreasing = TRUE)
        rank <- names(sortedprincipalVector)
        #rank[1]
        clusterSentences[as.numeric(rank[1])] 
      }else{
        print("inelse")
        clusterSentences[1]
      }
    }
    
    getSortedRankedSentences2 <- function(clusterSentences){
      # print(clusterSentences)
      if(length(clusterSentences) > 1){
        print("inif")
        corpusText1 <- VectorSource(clusterSentences)
        corpusText1 <- Corpus(corpusText1)
        corpus1 <- tm_map(corpusText1, content_transformer(tolower))
        corpus1 <- tm_map(corpus1, removePunctuation)
        corpus1 <- tm_map(corpus1, stripWhitespace)
        corpus1 <- tm_map(corpus1, removeWords, stopwords("english"))
        terms1 <- DocumentTermMatrix(corpus1,control = list(wordLengths=c(1,Inf), weighting=weightTfIdf))
        tfidf1 <- as.matrix(terms1)
        
        d1 <- dist(as.matrix(tfidf1))
        temp1 <- as.matrix(d1)
        
        eigenValues <- eigen(temp1)
        #eigenValues$values
        eigenvectors <- as.matrix(eigenValues$vectors)
        principalVector <- eigenvectors[,1]
        names(principalVector) <- seq(1:length(principalVector))
        sortedprincipalVector <- sort(principalVector, decreasing = TRUE)
        rank <- names(sortedprincipalVector)
        #rank[1]
        clusterSentences[as.numeric(rank[2])] 
      }else{
        print("inelse")
        abc <- " "
        abc
      }
    }
    
    summary <- c()
    clusterList <- list(cluster1Sentences, cluster2Sentences, cluster3Sentences, cluster4Sentences)
    clusterRank <- c()
    for(i in 1: length(clusterList)){
      clusterRank <- c(clusterRank, length(clusterList[[i]]))
    }
    
    names(clusterRank) <- seq(1:4)
    clusterRank <- sort(clusterRank, decreasing = TRUE)
    orderedClusterList <- list()
    ranking <- names(clusterRank)
    for(i in 1: length(ranking)){
      if(as.numeric(ranking[i]) == 1){
        summary<-c(summary,(getSortedRankedSentences(cluster1Sentences)))
      }else if(as.numeric(ranking[i]) == 2){
        summary<-c(summary,(getSortedRankedSentences(cluster2Sentences)))
      }else if(as.numeric(ranking[i]) == 3){
        summary<-c(summary,(getSortedRankedSentences(cluster3Sentences)))
      }else if(as.numeric(ranking[i]) == 4){
        summary<-c(summary,(getSortedRankedSentences(cluster4Sentences)))
      }
    }
    
    for(i in 1: length(ranking)){
      if(as.numeric(ranking[i]) == 1){
        summary<-c(summary,(getSortedRankedSentences2(cluster1Sentences)))
      }else if(as.numeric(ranking[i]) == 2){
        summary<-c(summary,(getSortedRankedSentences2(cluster2Sentences)))
      }else if(as.numeric(ranking[i]) == 3){
        summary<-c(summary,(getSortedRankedSentences2(cluster3Sentences)))
      }else if(as.numeric(ranking[i]) == 4){
        summary<-c(summary,(getSortedRankedSentences2(cluster4Sentences)))
      }
    }
    
    summaryToWrite <- c()
    lengthWritten <- 0
    for(i in 1:length(summary)){
      if(lengthWritten < 105){
        summaryToWrite <- c(summaryToWrite, summary[i])
        lineSum <- unlist(strsplit(summary[i], split = " "))
        lengthWritten <- lengthWritten + length(lineSum)
      }
    }
    write(summaryToWrite, outputFile)
  }
}