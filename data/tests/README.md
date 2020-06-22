## Data Cleaning Tests

Things done to check that the produced datasets are reasonable:

* Accounted for most prevalent marks in [CHAT manual](https://talkbank.org/manuals/CHAT.pdf). 
* Tested with hand-crafted CHAT file `tests.cha`. 
* Manually checked a random subset of produced utterances, checked for errors. 
* Ran basic sanity checks. 


### Sanity checks

- pass: Made test file to run script on, tests for correct result for specific inputs
- pass: Manually look at the pairs of inputs and outputs
- pass: Check that number of lines produced made sense (the number of lines + lines includes = total lines, etc.)
  - 2908641: Total utterances in Eng-NA corpora `grep -r "^grep -r "^\*" childes | wc -l\*" childes | wc -l` 
  - 2908629: Total gathered utterances `grep "^\"" processed/* | wc -l`
  - 2908577: Total cleaned utterances `cat all-utterances.txt | wc -l`
  - 1608317: Total accepted utterances: `cat data-split/outtput.txt | wc -l`
  - 1030982: Total primary target child utterances: `grep "CHI" all-utterances.txt | wc -l`
  - 138068: Total empty utterances: `grep -E "^\.|^\?|^\!" all-utterances.txt | wc -l`
- pass: Check for lines without punctuated endings
  - 0: `grep -v "[.?\!]" all-utterances.txt | wc -l`
- pass: Check for punctuation within lines
  - 0: `grep -E "\. |\! |\? " all-utterances.txt | wc -l`
- FAIL: Check for punctuation (,) at start of lines
- Check for numbers
- Check for lines with less than 5 characters
- Check for empty lines
- Check for non alphanumeric characters
- Look at some of the least frequent words


