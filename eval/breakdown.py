from nltk import CFG
import argparse

parser = argparse.ArgumentParser(description="break down results for analysis")

parser.add_argument('--data', type=str, default='output.txt', 
        help='path to file to analyze')

args = parser.parse_args()

with open("../gen/vocab-cfg.txt") as f:
    cfg_str = f.read()

cfg = CFG.fromstring(cfg_str)

aux_list = [str(x).split(' -> ')[1] for x in cfg.productions() if 'Aux' in str(x)]

targets = []
actuals = []
with open(args.data) as f:
    i = 0
    for line in f:
        if i % 2 == 0:
            targets.append(line)
        else:
            actuals.append(line)
        i += 1

def get_first_aux(words, aux_list):
    for word in words:
        if word in aux_list:
            return word
    return "no aux"

gfeim = 0 #gen first == input main
gfeif = 0 #gen first == input first
other = 0 
gfeim_list = []
gfeif_list = []
other_list = [] 
for i in range(0, len(targets)):
    target = targets[i].split()
    actual = actuals[i].split()
    if target[target.index('.') + 1] == actual[actual.index('.') + 1]:
        gfeim += 1
        gfeim_list.append(' '.join(actual))
    elif get_first_aux(target, aux_list) == actual[actual.index('.') + 1]:
        gfeif += 1
        gfeif_list.append(' '.join(actual))
    else:
        other += 1
        other_list.append(' '.join(actual))

print("gen first == input main: " + str(gfeim))
print("gen first == input first: " + str(gfeif))
print("other: " + str(other))
print("total: " + str(len(targets)))
print(other_list)
        
