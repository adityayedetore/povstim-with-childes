########################################################################
## Gathers the data and splits it into training, validation, and test 
## sets. 
##
## Produces directory split-data, containing output.txt, train.txt,  
## valid.txt, and test.txt. Additionally produces processed file
## gloss-and-filename.txt, for the purpose of making things run faster
## the second time around. 
##
## Steps: 1) Gather the non-child utterances (sentence) and the name of 
##           the files they came from. 
##        2) Shuffel by filename
##        2) Create a map from file name to number of utterances. 
##        3) Order map by frequency. 
##        4) Iterate through sets of n (=30) file names in map, randomly
##           assign one to be in the validation set, chose another to  
##           be the test set, and leave the remainder for the training 
##           set.  
##        5) Output the split data. 
##
## split.txt  - each utterance paired with file it came from, and 
##              which data set it will be used for
## output.txt - all the utterances 
## train.txt  - training set 
## valid.txt  - validation set
## test.txt   - test set
########################################################################

library(stringr)


if (!file.exists("gloss-and-filename.txt")) {
    print("====gathering data====")
    file.create("gloss-and-filename.txt")
    paths = list.files("processed", full.names=TRUE)
    for (p in paths) {
        print(p)
        utts<-read.table(file=p, header=TRUE)
        utts<-utts[,c("Speaker", "Gloss", "Filename")]
        utts<-utts[!(utts$Speaker=="CHI"),]
        utts<-utts[!(str_length(utts$Speaker)>5),]
        utts<-utts[!(str_length(utts$Gloss)==1),]
        w = utts[,c("Gloss", "Filename")]
        write.table(w, file="gloss-and-filename.txt", sep="\t", 
                    col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
    }
    print("gloss-and-filename.txt")
}
library(dplyr)


print("====reading data====")
data <- read.delim(file="gloss-and-filename.txt", header=FALSE)
colnames(data) <- c("Gloss", "Filename")

print("====assigning data====")
h <- as.data.frame(table(data$Filename))
h <- h[order(-h$Freq),]
Set <- rep("train", nrow(h))
n <- 30
for (i in seq(0, nrow(h) - n, n)) {
    s <- sample(1:n, 2, replace=FALSE)
    Set[s[1] + i] <- "valid"
    Set[s[2] + i] <- "test"
}
h$Set <- Set
data <- merge(data, h, by.x = "Filename", by.y = "Var1", all.x = TRUE, all.y = FALSE)

print("====shuffling data====")
data %>% 
    group_by(Filename) %>%
    group_split() %>%
    sample() -> data_split
file.create("tmp.txt")
for (w in data_split) {
    write.table(w, file="tmp.txt", sep="\t", 
                col.names=FALSE, row.names=FALSE, quote=FALSE, append=TRUE)
}
data <- read.delim(file="tmp.txt", header=FALSE)
colnames(data) <- c("Filename", "Gloss", "Freq", "Set")
file.remove("tmp.txt")

print("====saving data====")
if(!dir.exists("split-data"))
   dir.create("split-data")
write.table(data[,c("Gloss", "Filename", "Set")], file="split-data/split.txt", 
            sep="\t", col.names=FALSE, row.names=FALSE, quote=FALSE, append=FALSE)
print("split-data/split.txt")
write.table(data[,"Gloss"], file="split-data/output.txt", sep="\t", 
            col.names=FALSE, row.names=FALSE, quote=FALSE, append=FALSE)
print("split-data/output.txt")
write.table(subset(data, Set=="train")[,"Gloss"], file="split-data/train.txt", 
            sep="\t", col.names=FALSE, row.names=FALSE, quote=FALSE, append=FALSE)
print("split-data/train.txt")
write.table(subset(data, Set=="valid")[,"Gloss"], file="split-data/valid.txt", 
            sep="\t", col.names=FALSE, row.names=FALSE, quote=FALSE, append=FALSE)
print("split-data/valid.txt")
write.table(subset(data, Set=="test")[,"Gloss"], file="split-data/test.txt", 
            sep="\t", col.names=FALSE, row.names=FALSE, quote=FALSE, append=FALSE)
print("split-data/test.txt")
