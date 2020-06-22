# Data for model training

This directory contains scripts that remove the CHAT formatting from NA-Eng CHILDES transcripts, producing a clean data set for training our language model. 

## Gathering the data

The data comes from CHILDES. We used the [Eng-NA](https://childes.talkbank.org/access/Eng-NA/) corpus. You download the corpora I used [here](http://adityayedetore.com/data/childes). 

Note that the  [Nadig](https://talkbank.org/access/ASDBank/English/Nadig.html) corpus access page was not functional as of May 2020. It was therefore excluded.

*ADD CITATIONS*

## Cleaning the data

The code for transforming the data from CHAT transcription to normal text has been adapted from [Melissa Kline's CLANtoR](https://github.com/mekline/CLANtoR).*ADD CITATION*  You can download the produced datasets [here](https://adityayedetore.com/data/processed). Alternatively download the [raw data I used](https://adityayedetore.com/data/childes) or the individual corpora from the [CHILDES talkbank website](https://childes.talkbank.org/access/Eng-NA/). 

* `CLANtoR.R` formats the CHAT transcription as a data frame. 
* `childes-to-tsv.R` calls the functions in `CLANtoR.R` on all `*.cha` files in `childes` directory and saves the tab separated value files to `processed`, overwriting previous files. Expects `childes` directory containing the CHAT formatted data. 
* `tsv-to-utterances.R` gathers the utterances from all the formatted data and saves them to `output.txt`. Also produces `gloss-and-filename.txt` for use with `utts-to-training.R`. Expects `processed` directory containing output of calling `collect-data.R`. 
* `utts-to-training.R` splits the utterances into training, validation, and test sets. Calls `tsv-to-utterance.R` if `gloss-and-filename.txt` not found. 

### Marks removed and kept

* `tests/test.csv` implicitly details what was remove and what was kept from the CHAT transcriptions. Basically, any decisions made were made to ensure that the training data more accurately reflect what the child would have heard. So for instance, the transcription _(be)cause_, which indicates that non-completion of the word _because_, is kept as _cause_. In addition, all extraneous marks were removed. 
* `tests/test.cha` and `tests/test.txt` contain CHAT formatted testing text and the proper output when `collect-data.R` is called on `tests`, respectively. 
* `run-tests.R` processes `tests` as if it were a corpus, produces `results.txt`, which can be compared to `tests/test.csv` or `tests/tests-correct.txt`.


[CHAT Transcription Format Guide](https://talkbank.org/manuals/CHAT.html#_Toc33781487) has information about the meanings of the marks in the CHAT format.  This is the citation they would like us to use: MacWhinney, B. (2000). The CHILDES project: Tools for analyzing talk. 3rd edition. Mahwah, NJ: Lawrence Erlbaum Associates.

### Full description of data gathering process

1. Downloaded (almost) all the data from the Eng-NA corpora. 
  - Didn't use one of them, it wasn't available last time I checked

2. Cleaned the data 
  - Removed all the transcription marks 
  - Removed all utterances of length 1 or 0 chars  
  - Removed all utterances by target children 

3. Tested the scripts, checked the data
  - Tests can be found in `tests` directory. 

4. Split the data
    1. Gather the non-child utterances and corresponding filenames.
    2. Shuffel by filename. 
    3. Create a map from file name to number of utterances.
    4. Order map by number of utterances. 
    5. Iterate through sets of n (=30) file names in map, randomly assign one to the validation set, another to the test set, and leave the remainder for the training set.
    6. Split data by assignments. 
