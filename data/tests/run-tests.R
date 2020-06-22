###############################################################################
## Produces test-results.txt. 
###############################################################################


source("../CLANtoR.R")
library(gsubfn)
library(stringr)

filenames <- list.files(pattern="*.cha")
d <- lapply(filenames, read.CLAN.file)
mydata <- rbind.fill(d)
orig.length <-nrow(mydata)
origdata <- mydata

###################################################

out_filename = "results.txt" 
file.create(out_filename)
#this gives you an excel-style file with as many columns as column names)
write.table(mydata, file=out_filename, sep="\t", col.names = NA)

