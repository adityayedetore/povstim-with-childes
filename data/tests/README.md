## Data Cleaning Tests

(!!!) This README should be expanded on once I've finished doing the testing

Things done to check that the produced datasets are reasonable:

* Accounted for most prevalent marks in [CHAT manual](https://talkbank.org/manuals/CHAT.pdf). 
* Tested with hand-crafted CHAT file `tests.cha`. 
* Manually checked a random subset of produced utterances, checked for errors. 
* Ran basic sanity tests. 

### Manual Checking

List of the documents I checked:

* childes/Bates/Free28/jane.cha
  - &-
* childes/Bates/Free28/keith.cha
* childes/Bates/Free20/zeke.cha
* childes/Bates/Free20/kathy.cha

* childes/Bernstein/Children/Dale/010700.cha
  - (.) indicates a pause, should that be kept? 
* childes/Bernstein/Children/Kay/010400.cha
  - oh , Kay would like to speak to you (.) say hi , Scott .
  - (.) oh , thank you .
  - (.) Kay , that's a house (.) can you say house ?
* childes/Bernstein/Children/Amelia/010600.cha
  - this's the door (..) and there's the block !
* childes/Bernstein/Children/Amelia/010800.cha
  - pull hard , (.) unzip the pants . 
  - that's an owl (.) oh , the blocks fell over . 
  - and see , he's gonna (.) shave his face , see ? 
* childes/Bernstein/Interview/anne3.cha
  - I was afraid to hold her off , because we're going away on Friday , for vacation and I (.) hated to delay you .
* childes/Bernstein/Children/Cindy/010800.cha
  - &hah ?  -> ?
  - (a)n(d) pull it down .  -> nd pull it down .

* childes/Bliss/norjusti.cha
* childes/Bliss/noraimee.cha 624/2334
  - +, mushamusha@o mush +... -> , mushamusha mush ...

* childes/Bloom70/Peter/020010.cha ~3000/70000

* childes/Bloom73/010714.cha ~800 / 5000

* childes/Bohannon/Bax/russ.cha 676 / 10000
* childes/Bohannon/Nat/harvey.cha 1400 / 10000

* childes/Braunwald/020215.cha 300 / 80000
* childes/Braunwald/020023.cha 150 / 80000
  - and you don't have a crib , , do you ? 
* childes/Braunwald/020120.cha 400 / 80000
  - I 0will  tell you . -> I will tell you

* childes/Brent/c1/000917.cha 1739 / 168042
  - &aw , sweetie . -> , sweetie .
* childes/Brent/c1/000930.cha 1000 / 168042

* childes/Brown/Adam/020304.cha
  - Hum(pty)z_Dum(pty) .	Humz Dumpty .

Stuff to change: 

* find and replace (.) with PAUSE, (..) with PAUSE2, etc. 
* Remove &-
* Find and remove +, 
* maybe deal with (a)n(d)
* replace ", ," with ","
* Think about dealing with interruption +/
* Maybe deal with 0word meaning omitted word (probably not)
* Figure out what to do with just & as in &aw
* Underscores should removed prior. In general remove the superfluous stuff first. 

### Sanity Tests

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


