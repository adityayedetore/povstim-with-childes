
## Fine Tuning

This README needs to be cleaned up. I should detail the fine tuning process, and what the data is like (link to `data/tune`). 

```
python main.py --data tune-data --epochs 4 --save "model.pt~tuned" --log tune-log.txt 
```

batch size should be 1, bptt doesn't matter

Edits I made: 
- The model is now initialized by the pre-trained model `model.pt`. 
    - In the build the model section of `main.py`
- The `init_hidden` function in `train()` is always passed `1`. 

- The loop for training is now sentence by sentence, instead of batch by batch. 

in `dictionary_corpus.py`, when a file is converted indices, after each line there is a [-1] index. This is for purposes of splitting later. 



I excluded 20% of the files in the CHILDES Treebank from the pre-training, used those for the test set of the fine tuning. 
