# Script to generate sentences from a language model. 
#
# Alternatively, interactively generate sentences or 
# and/or evaluate them
# 
# Aditya Yedetore, 5/26/2020

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import repackage_hidden, batchify, get_batch
import dictionary_corpus
import numpy as np
import random

parser = argparse.ArgumentParser(description='Generates sentences from trained model')
parser.add_argument('--gen', type=int, default=0,
        help='number of sentences to generate')
parser.add_argument('--eval', type=str, default="none",
        help='path to file to evaluate on')
parser.add_argument('--interactive', action='store_true', 
        help='word by word interactive mode')
parser.add_argument('--model', type=str, default="model.pt",
        help="path to model to evaluate on")
parser.add_argument("--recall_k", type=int, default=10, 
        help="top k to check")
parser.add_argument('--results', type=str, default='results.txt',
        help="path to store eval results")
parser.add_argument("--cuda", action='store_true',
        help="use cuda")
args = parser.parse_args()

def generate(hidden, dictionary, model):
    i = args.gen
    word = input("first word: ")
    indices = list(range(0, len(dictionary)))
    f = open('gen-sents.csv', 'w')
    f.write("text\n\"" + word + ' ' )
    while(i > 0):
        data = torch.tensor([[dictionary.word2idx[word]]])
        output, hidden = model(data, hidden)
        o = output.numpy()[0][0]
        index = random.choices(indices, weights = o, k = 1)[0]
        word = dictionary.idx2word[index]
        f.write( word + ' ')
        if word == "." or word == "?" or word == "!":
            f.write("\"\n\"")
            i = i - 1
    f.close()
    print("Remember to remove the extra \" from the bottom of the csv")

def interactive(word, dictionary, hidden, model):
    while(word != "quit"):
        word = input("word: ")
        word = word.strip()
        if (word not in dictionary.word2idx):
            print("<unk>")
            word = "<unk>"
        data = torch.tensor([[dictionary.word2idx[word]]])
        output, hidden = model(data, hidden)
        o = output.numpy()[0][0]
        idx = np.argpartition(o, -10)[-10:] # get 10 most likely 
        idx = idx[np.argsort(o[idx])] # sort by likelihood and reverse
        idx = idx[::-1]
        for x in idx:
            print("\t" + dictionary.idx2word[x] + "\t" 
                    + str(o[x]))

def auto_eval(dictionary, hidden, model):
    f = open(args.eval, "r")
    ratings = []
    preds = []
    count = 0
    print("recall@" + str(args.recall_k))
    for line in f:
        for word in line.split():
            if (word not in dictionary.word2idx):
                word = "<unk>"
            data = torch.tensor([[dictionary.word2idx[word]]])
            if args.cuda:
                data = data.cuda()
            output, hidden = model(data, hidden)
            output = output.cpu()
            o = output.numpy()[0][0]
            idx = np.argpartition(o, -args.recall_k)[-args.recall_k:] 
            idx = idx[np.argsort(o[idx])]
            idx = idx[::-1]
            ratings.append(int(word in preds))
            preds = [dictionary.idx2word[x] for x in idx]
            count = count + 1
            if count % 1000 == 0:
                print(str(np.mean(ratings)))
    print("final average: " + str(np.mean(ratings)))
    with open(args.results, 'w') as f:
        f.write("final average: " + str(np.mean(ratings)))

with open(args.model, 'rb') as f:
    if args.cuda:
        model = torch.load(f)
    else:
        import warnings
        warnings.filterwarnings("ignore")
        model = torch.load(f, map_location = lambda storage, loc: storage)

if args.cuda:
    model.cuda()

model.eval()
total_loss = 0
eval_batch_size = 1
hidden = model.init_hidden(eval_batch_size)
dictionary = dictionary_corpus.Dictionary("CHILDES")
with torch.no_grad():
    if args.interactive:
        interactive(word = "", hidden = hidden, dictionary = dictionary, model = model)
    elif args.eval != "none":
        auto_eval(hidden = hidden, dictionary = dictionary, model = model)
    elif args.gen: 
        generate(hidden = hidden, dictionary = dictionary, model = model)
    else:
        parser.print_help()

