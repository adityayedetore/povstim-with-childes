#######################################################################
## Script to collect all the utterances from the files produced 
## by calling collect-data.R
##
## Removes CHI utterances and utterances with no content (e.g. "."
## utterances)
##
## Produces:
##   all-utterances.txt - all the utterances
##   gloss-and-filename.txt - utterances and filename
##
## Overwrites previous files. 
#######################################################################

library(stringr)

is_child <- function(row) {
    s = str_trim(row["Speaker"])
    p = trimws(strsplit(row["Participants"], " , "))
    search_string = paste(s, ".*Target_Child", sep="")
    sum(grepl(search_string, p)) > 0
}

print("====gathering data====")
file.create("gloss-and-filename.txt")
file.create("all-utterances.txt")
paths = list.files("processed", full.names=TRUE)
for (p in paths) {
    print(p)
    master<-read.table(file=p, header=TRUE)
    utts<-master[,c("Speaker", "Gloss", "Filename", "Participants")]
    utts<-utts[!(str_length(utts$Gloss)<=1),]
    utts<-utts[!apply(utts, 1, is_child),]
    write.table(utts[,c("Gloss", "Filename")], 
                file="gloss-and-filename.txt", sep="\t",
                col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
    write.table(master[,c("Gloss", "Filename", "Speaker")], 
                          file="all-utterances.txt", sep="\t", 
                          col.names=FALSE, row.names=FALSE, 
                          quote=FALSE, append=TRUE)
}
print("produced gloss-and-filename.txt")
print("produced all-utterances.txt")
