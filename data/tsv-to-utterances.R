#######################################################################
## Script to collect all the utterances from the files produced 
## by calling collect-data.R
##
## Removes CHI utterances and utterances with no content (e.g. "."
## utterances)
##
## Produces:
##   output.txt - the utterances only
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
file.create("output.txt")
paths = list.files("processed", full.names=TRUE)
for (p in paths) {
    print(p)
    utts<-read.table(file=p, header=TRUE)
    utts<-utts[,c("Speaker", "Gloss", "Filename", "Participants")]
    utts<-utts[!apply(utts, 1, is_child),]
    utts<-utts[!(str_length(utts$Speaker)>5),]
    utts<-utts[!(str_length(utts$Gloss)<=1),]
    w = utts[,c("Gloss", "Filename")]
    write.table(w, file="gloss-and-filename.txt", sep="\t",
                col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
    write.table(utts$Gloss, file="output.txt", sep="\t", 
                col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
}
print("produced gloss-and-filename.txt")
print("produced output.txt")
