###############################################################################
## This is example code that will collect the data in the childes corpus using
## CLANtoR.R
##
## 
## The code will search for the directory 'childes', and will parse all
## the .cha files in each subdirectory of 'childes'. 
## Outputs are in processed/, and each is called childes-Subdirectory.txt
##
## Running this code on all the Eng-NA corpora takes ~2 hours 
##
###############################################################################


source("CLANtoR.R")
library(gsubfn)
library(stringr)

paths <- list.dirs(path="childes", recursive=FALSE)
n <- length(paths)
start_number <- 1
#for (p in c("tests") ) { # for testing purposes
print(paths)
for (p in paths[start_number:n]) { # for
    print(paste(start_number, p, sep=" : "))
    start_number <- start_number + 1
    filenames <- list.files(path=p, pattern="*.cha", recursive=TRUE, full.names=TRUE)
    d <- lapply(filenames, read.CLAN.file)
    mydata <- rbind.fill(d)
    orig.length <-nrow(mydata)
    origdata <- mydata

    ###################################################

    #Save the output file in in processed directory
    setwd("processed")
    out_filename = paste(gsub("/", "-", p), ".txt", sep="")
    file.create(out_filename)
    #this gives you an excel-style file with as many columns as column names)
    write.table(mydata, file=out_filename, sep="\t", col.names = NA)
    setwd("../")
}

