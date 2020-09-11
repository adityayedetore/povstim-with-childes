from nltk import CFG
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="break down results for analysis")

parser.add_argument('--data', type=str, default='none', 
        help='path to file to analyze')
parser.add_argument('--out', type=str, default='output.txt',
        help='path to output results')

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
            targets.append(line[7:-1])
        else:
            actuals.append(line[7:-1])
        i += 1

def get_first_aux(words, aux_list):
    for word in words:
        if word in aux_list:
            return word
    return "no aux"

index=range(0, len(targets))
columns=['target','actual', 'target_main_aux', 'target_first_aux', 
        'actual_main_aux', 'move_main_aux', 'move_first_aux', 'move_other_aux']
df = pd.DataFrame(index=index, columns=columns)
df['target'] = targets
df['actual'] = actuals

for i in range(0, len(targets)):
    target = df['target'][i].split()
    actual = df['actual'][i].split()
    df['target_main_aux'][i] = target[target.index('.') + 1]
    df['target_first_aux'][i] = get_first_aux(target, aux_list)
    df['actual_main_aux'][i] = actual[actual.index('.') + 1]
    df['move_main_aux'][i] = int(df['target_main_aux'][i] == df['actual_main_aux'][i])
    df['move_first_aux'][i] = int(df['target_first_aux'][i] == df['actual_main_aux'][i])
    df['move_other_aux'][i] = int((not df['move_main_aux'][i]) and (not df['move_first_aux'][i]))


df.to_csv(args.out)
