###############################################################
## Adapted from Melissa's R converter for CHILDES-CLAN files. 
## There were meny errors in the creation of the Gloss, 
## I have attempted to fix them. 
## For all the Eng-NA corpora, it takes ~2 hours
##
## Note that the part I've changed most is the processing of
## the Gloss. Before it was seperated into Gloss and 
## CleanGloss, now there is only Gloss. Also, this code will 
## not do any of the replacements of the origonal code. 
## 
## Below are the Melissa's original comments
##
###############################################################

###############################################################
## This is an R function that takes a single CLAN-formatted
## corpus file (*.cha) and returns a dataframe.  Takes <30s
## per file, around 10 min for the Eve(Brown) Corpus.  
##
## The dataframe has a row for each sentence in the corpus, with the 
## following columns:
##
## From the file header & child participant annotation:
## FileName
## Participants (A string with the full list)
## Language 
## Corpus
## Age (child's)
## Gender (ditto)
## Date
## File.Situation
## 
## From the line itself
## Speaker
## Verbatim sentence
## Tiers: any that we find!
## 
## Also includes a gloss calculated from the utterance line, which
## gets rid of clarification sequences ("a bobby [= a thin bobbypin]" -> "a bobby")
## replaces 1-word glosses ("dunno [: don't know]" -> "don't know"), and
## cleans up various CHILDES-internal markup.  Ideally, this yields a gloss
## with the same number of words as the mor line. 
##
## This gloss is designed for presenting sentences to adult readers, though
## the form given may still want some processing (deleting sentence-final
## space, replacing internal "." with ",", continuation "+...") - these are left
## as-is here for ease of alignment against the mor and other tiers.
## Watch out for "," '"' and "'" when converting to/from csv
###############################################################

library(plyr)

read.CLAN.file <- function(f) {
	tmp <- readLines(f)
	if (length(tmp) < 20) {
		# This checks for dummy files and empty files
		return(data.frame())
	}
	# Cycle through utterances and make a line for each.
	alltext <- paste(tmp, collapse="\n")
	utts <- unlist(strsplit(alltext, "\n\\*"))
	utts <- utts[-1]
	tierlist <- lapply(utts, get_utt_info)
	data <- rbind.fill(tierlist)
	
	#Collect the data that will be appended to every line
	data$Filename <- f
	
	p <- grep("@Participants", tmp, fixed=TRUE)
	data$Participants <- unlist(strsplit(tmp[p], "\t"))[2]
	
	p <- grep("@Date", tmp, fixed=TRUE)
	data$Date <- unlist(strsplit(tmp[p], "\t"))[2]
	
	p <- grep("@Situation", tmp, fixed=TRUE)
	data$File.Situation <- unlist(strsplit(tmp[p], "\t"))[2]
	
	p <- grep("Target_Child", tmp, fixed=TRUE)
	chiline <- tmp[p[2]]
	chidata <- unlist(strsplit(chiline, "[|]"))
	data$Language <- substr(chidata[1], 6,9)
	data$Corpus <- chidata[2]
	data$Age <- chidata[4]
	data$Gender <- chidata[5]
	
	#Add utt line numbers
	data$Line.No 

		
	#Get rid of some yucky processing columns we don't want
	data$t.as.matrix.fields.. <- NULL
	xnums <- as.numeric(gsub("[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]+", "", names(data), perl=T)) 		# what a hack
	if (length(xnums[!is.na(xnums)]) != 0) {
		for(x in min(xnums, na.rm=T):max(xnums, na.rm=T)) {
			xname <- paste("X", x, sep="")
			data <- data[,!(names(data) %in% xname)]
		}
	}
	
	#Make sure row names are preserved!
	data$Utt.Number <- row.names(data)
	
	#Return
	data
} #End read.CLAN.file

get_utt_info <- function(u){
	#remove "[*]"
	u = gsub("\\[\\*\\]", "", u)
	#Divide the line into individual utterances & tiers
	fields <- unlist(strsplit(u, "\n%|\n@"))
	#Make a dataframe
	myrow <- data.frame(t(as.matrix(fields)))
	
	#Add utterance info
	divloc = gregexpr(":", fields[1])[[1]][1] - 1
	myrow$Speaker <- substr(fields[1], 1, divloc)
	myrow$Verbatim <- substr(fields[1], divloc + 3, nchar(fields[1]))
	myrow$Gloss <- NA
	
	#Add info from any tiers, as they appear in the file
	if (length(fields) > 1){
		for (j in 2:length(fields)){
			divloc = gregexpr(":", fields[j])[[1]][1] - 1
			if (divloc > 0) {
				tier <- data.frame(substr(fields[j], divloc + 3, nchar(fields[j])))
				names(tier) <- c(substr(fields[j], 1, divloc))
				myrow <- cbind(myrow, tier)
			}
		}
	}
	
	#The rest is to clean up the gloss

	# Add a space before punctuated marks at word ends
	wordsString = myrow$Verbatim
	wordsString  = gsub("[", " [", wordsString, fixed=TRUE)
	wordsString  = gsub("", " ", wordsString, fixed=TRUE)

	myrow$Gloss <- NA
	words <- unlist(strsplit(wordsString, " "))
	if (length(words) == 0){
		words <- c("")
	}
	
	words <- unlist(strsplit(words, "\t"))
	if (length(words) == 0){
		words <- c("")
	}
	
	words <- unlist(strsplit(words, "\n", fixed=TRUE))
	if (length(words) == 0){
		words <- c("")
	}

	#Next, find & replace clarification/elaboration sequences like this: "a bobby [= a thin bobbypin]" -> "a bobby"
	w <- 1
	wmax <- length(words) + 1
	while (w < wmax){
		#Did we hit a gloss sequence?
		if ((substr(words[w],1,1) == "[")){
			#Find where the gloss ends, then clean up
			closebracket <- grep("]",  words[w:length(words)], fixed=TRUE)[1] + (w-1)
			for (v in w:closebracket){
				words[v] <- ""
			}
		}
		w <- w + 1	
	}

	#Next, find & replace notes like this : "test@dog " -> "test" or "test&dog " -> "test"
	w <- 1
	wmax <- length(words) + 1
	while (w < wmax){
		#Did we hit a '@' char? 
		if (gregexpr("[@&]", words[w])[[1]][1] > 0 ){
			#Find where the word ends, then clean up
			words[w] = substr(words[w], 1, gregexpr("[@&]", words[w])[[1]][1] - 1)
		}
		w <- w + 1	
	}
	#Next, find & replace stuff like this : "te(dog)st " -> "test"
	w <- 1
	wmax <- length(words) + 1
	while (w < wmax){
		#Did we hit a '(' char? 
		if (gregexpr("[(]", words[w])[[1]][1] > 0 ){
			#Find where the word ends, then clean up
				words[w] = paste(substr(words[w], 1, gregexpr("[(]", words[w])[[1]][1] - 1), 
					substr(words[w], gregexpr("[)]", words[w])[[1]][1] + 1, str_length(words[w])),
					sep="")
		}
		w <- w + 1	
	}
	w <- 1
	wmax <- length(words) + 1
	while (w < wmax){
		#Did we hit a '' char?
		if (gregexpr("", words[w])[[1]][1] > 0 ){
			 words[w] = ""
		}
		w <- w + 1
	}
	
	myrow$Gloss <- paste(words, collapse=" ")
	myrow$Gloss <- gsub(" +", " ", myrow$Gloss, fixed=TRUE)
	myrow$Gloss <- gsub("[];0()<>&@:\\+\\^]", "", myrow$Gloss)
	myrow$Gloss <- gsub("_", " ", myrow$Gloss, fixed=TRUE)
	myrow$Gloss <- gsub("/", "", myrow$Gloss, fixed=TRUE)
	myrow$Gloss <- gsub("\"", "", myrow$Gloss)
	myrow$Gloss <- gsub("\\\\", "", myrow$Gloss)
	myrow$Gloss <- gsub("[ˈ↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ∲§∾↻Ἡ„‡ạʰāʔʕš“”/↑↓↫-]", "", myrow$Gloss)
	myrow$Gloss  = gsub("\\>\\.", " .", myrow$Gloss )
	myrow$Gloss  = gsub("\\>\\?", " ?", myrow$Gloss )
	myrow$Gloss  = gsub("\\>\\!", " !", myrow$Gloss )
	myrow$Gloss  = gsub("\\>\\,", " ,", myrow$Gloss )
	myrow$Gloss <- str_squish(myrow$Gloss)
	
	#Return
	myrow
	
} #END get_utt_info
