###############################################################################
## Same code as collect-data.R, but instead called on tests directory, 
## which contains the test.cha file. Produces test-results.txt. 
###############################################################################


source("CLANtoR.R")
library(gsubfn)
library(stringr)

paths <- list.dirs(path="childes", recursive=FALSE)
n <- length(paths)
output_number <- 1
for (p in c("tests") ) { # for testing purposes
#for (p in paths) { # for
    print(paste(output_number, p, sep=" : "))
    output_number <- output_number + 1
    filenames <- list.files(path=p, pattern="*.cha", recursive=TRUE, full.names=TRUE)
    d <- lapply(filenames, read.CLAN.file)
    mydata <- rbind.fill(d)
    orig.length <-nrow(mydata)
    origdata <- mydata

    ###################################################

    #Save the output file in in processed directory
    out_filename = paste(gsub("/", "-", p), "-results.txt", sep="")
    file.create(out_filename)
    #this gives you an excel-style file with as many columns as column names)
    write.table(mydata, file=out_filename, sep="\t", col.names = NA)
}

