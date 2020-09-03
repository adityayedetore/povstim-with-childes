This directory contains the scripts I used to evaluate the CHILDES language model. 

You can use your `model.pt` or download our [pre-trained best model](http://adityayedetore.com/data/model.pt). 

To use these scripts, download our [vocabulary](http://adityayedetore.com/data/CHILDES) (also downloads our training data). 

`python eval.py --eval "../gen/decl-quest-test-set.txt" --model ../tune/fine-tuned/models/fine-tuned/1095.pt --results "results/1095-1000-test-results.txt" --n 1000 --summary "results/1095-1000-test-summary.txt"`
