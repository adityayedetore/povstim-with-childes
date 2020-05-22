# Data for model training

This directory contains scripts that remove the CHAT formatting from NA-Eng CHILDES transcripts, producing a clean data set for training our language model. 

## Gathering the data

The data comes from CHILDES. We used the [Eng-NA](https://childes.talkbank.org/access/Eng-NA/) corpus. You download the corpora I used [here](http://adityayedetore.com/data/childes). 

Note that the  [Nadig](https://talkbank.org/access/ASDBank/English/Nadig.html) corpus access page was not functional as of May 2020. It was therefore excluded.

*ADD CITATIONS*

## Cleaning the data

The code for transforming the data from CHAT transcription to normal text has been adapted from [Melissa Kline's CLANtoR](https://github.com/mekline/CLANtoR).*ADD CITATION*  You can download the produced datasets [here](http://adityayedetore.com/data/processed). 

* `CLANtoR.R` formats the CHAT transcription as a data frame. 
* `collect-data.R` calls the functions in `CLANtoR.R` on all `*.cha` files in `childes` directory and saves them in `processed`. Expects `childes` directory containing the CHAT formatted data. 
* `get-utterances.R` gathers the utterances from all the formatted data and saves them to `output.txt`. Expects `processed` directory. 


### Marks removed and kept

* `tests/test.csv` details what was remove and what was kept from the CHAT transcriptions. Basically, any decisions made were made to ensure that the training data more accurately reflect what the child would have heard. So for instance, the transcription _(be)cause_, which indicates that non-completion of the word _because_, is kept as _cause_. In addition, all extraneous marks were removed. 
* `tests/test.cha` and `tests/test.txt` contain CHAT formatted testing text and the proper output when `collect-data.R` is called on `tests`, respectively. 
* `tests.R` processes `tests` as if it were a corpus, produces `tests-results.txt`, which can be compared to `tests/test.csv` or `tests/tests-correct.txt`.


[CHAT Transcription Format Guide](https://talkbank.org/manuals/CHAT.html#_Toc33781487) has information about the meanings of the marks in the CHAT format.  This is the citation they would like us to use: MacWhinney, B. (2000). The CHILDES project: Tools for analyzing talk. 3rd edition. Mahwah, NJ: Lawrence Erlbaum Associates.
