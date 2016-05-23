library("tm")
setwd("E:/IIT KHARAGPUR/Semester II/Complex Networks/Project/workspace")
filesC <- list.files(path = "./summary/", pattern = NULL, all.files = FALSE,
                    full.names = FALSE, recursive = T,
                    ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)
filesp <- list.files(path = "./summaryp/", pattern = NULL, all.files = FALSE,
                     full.names = FALSE, recursive = T,
                     ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)

for(i in 1:length(filesP)){
  if(filesp[i] %in% filesC){
    outputFile <- substr(filesp[i],1,nchar(filesp[i])-4) 
    outputFile <- paste("./merged/", filesp[i] , sep = "")
    file1loc <- paste("./summary/", filesp[i], sep = "")
    file2loc <- paste("./summaryp/", filesp[i], sep = "")
    file1 <- readLines(file1loc)
    file2 <- readLines(file2loc)
    datatowrite <- c(file1, file2)
    datatowrite <- paste(datatowrite, collapse = " ")
    write(datatowrite, outputFile)
  }
}


##########################################################################
