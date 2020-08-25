# Script to evaluate language model 
#
# Aditya Yedetore, 8/2020

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import repackage_hidden
import dictionary_corpus
import numpy as np

parser = argparse.ArgumentParser(description='Generates sentences from trained model')
parser.add_argument('--eval', type=str, default="none",
        help='path to file to evaluate on')
parser.add_argument('--model', type=str, default="model.pt",
        help="path to model to evaluate on")
parser.add_argument('--results', type=str, default="results.txt", 
        help="path to saved results")
parser.add_argument('--summary', type=str, default="summary.txt",
        help="path to performance summary")
parser.add_argument('--n', type=int, default=1000,
        help="max sentences to evaluate on")
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
args = parser.parse_args()

def auto_eval(dictionary, hidden, model):
    total = 0
    first_correct = 0
    full_correct = 0
    with open(args.eval, "r") as f:
        eva = f.readlines()

    with open(args.results, 'w') as f:
        for line in eva:
            total += 1
            hidden = model.init_hidden(1)
            words = line.split()
            for i, word in enumerate(words[:words.index(".") + 1]):
                if (word not in dictionary.word2idx):
                    word = "<unk>"
                data = torch.tensor([[dictionary.word2idx[word]]])
                output, hidden = model(data, hidden)

            o = output.numpy()[0][0]
            o = np.array(output[0][0])
            idx = np.argpartition(o, -1)[-1:][0] # get most likely 
            pred = dictionary.idx2word[idx]
            pred_sent = pred
            target = words[words.index(".") + 1]
            first_correct += int(pred == target)
            
            i = 0
            while(pred != "?"):
                word = pred
                data = torch.tensor([[dictionary.word2idx[word]]])
                output, hidden = model(data, hidden)
                o = output.numpy()[0][0]
                o = np.array(output[0][0])
                idx = np.argpartition(o, -1)[-1:][0] # get most likely 
                pred = dictionary.idx2word[idx]
                pred_sent += " " + pred
                i += 1
                if i > 50:
                    break
            pred_sent = ' '.join(words[:words.index(".") + 1]) + ' ' + pred_sent + "\n"
            f.write("target: " + line + "actual: " + pred_sent + "\n")

            if (pred_sent == line):
                full_correct += 1

            if total > args.n:
                break


    with open(args.summary, "w") as f:
        f.write("first word correct: " + str(first_correct) + "/" + str(total-1) + "\n")
        f.write("full sent correct: " + str(full_correct) + "/" + str(total-1) + "\n")


with open(args.model, 'rb') as f:
    print("Loading the model")
    if args.cuda:
        model = torch.load(f)
    else:
        import warnings
        warnings.filterwarnings("ignore")
        model = torch.load(f, map_location = lambda storage, loc: storage)

model.eval()
if args.cuda:
    model.cuda()
else:
    model.cpu()
total_loss = 0
hidden = model.init_hidden(1)
dictionary = dictionary_corpus.Dictionary("CHILDES")
with torch.no_grad():
    auto_eval(hidden = hidden, dictionary = dictionary, model = model)

