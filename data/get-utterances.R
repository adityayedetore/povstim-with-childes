#######################################################################
## Script to collect all the utterances from the files produced 
## by calling collect-data.R. 
##
## The only processing done here is to remove the utterances of the 
## child, and to remove the utterances that have no content (e.g. 
## "." utterances)
##
## The utterances are output to output.txt
#######################################################################

library(stringr)

get_utterances <- function(f) {
    somedata <- read.table(file=f, header=TRUE)
    return(somedata[,c("Speaker", "Gloss")])
}

file.create("output.txt")
paths = list.files("processed", full.names=TRUE)
output = c()
for (p in paths) {
    print(p)
    utts =  get_utterances(p)
    utts<-utts[!(utts$Speaker=="CHI"),]
    utts<-utts[!(str_length(utts$Speaker)>5),]
    utts<-utts[!(str_length(utts$Gloss)==1),]
    utts$Speaker = as.character(utts$Speaker)
    write.table(utts$Gloss, file="output.txt", sep="\t", 
                col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
}
