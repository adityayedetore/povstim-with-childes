import argparse
import pandas as pd
from collections import defaultdict

parser = argparse.ArgumentParser(description="break down results for analysis")

parser.add_argument('--data', type=str, default='none', 
        help='path to file to analyze')
parser.add_argument('--out', type=str, default='output.txt',
        help='path to output results')

args = parser.parse_args()

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

aux_list = [x.split() for x in targets]
aux_list = list(set(x[x.index('.') + 1] for x in aux_list))
aux_list.sort()

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
acc_by_aux = defaultdict(int)
for i in range(0, len(targets)):
    target = df['target'][i].split()
    actual = df['actual'][i].split()
    df['target_main_aux'][i] = target[target.index('.') + 1]
    df['target_first_aux'][i] = get_first_aux(target, aux_list)
    df['actual_main_aux'][i] = actual[actual.index('.') + 1]
    df['move_main_aux'][i] = int(df['target_main_aux'][i] == df['actual_main_aux'][i])
    df['move_first_aux'][i] = int(df['target_first_aux'][i] == df['actual_main_aux'][i])
    df['move_other_aux'][i] = int((not df['move_main_aux'][i]) and (not df['move_first_aux'][i]))
    acc_by_aux[df['target_main_aux'][i]] += df['move_main_aux'][i]
    acc_by_aux[df['target_main_aux'][i] + '~total'] += 1

df.to_csv(args.out)

with open(args.out + '~summary', 'w') as f:
    for aux in aux_list:
        f.write(aux + ": \t" + str(acc_by_aux[aux]/acc_by_aux[aux + '~total'])[:10] + 
                "\t" + str(acc_by_aux[aux]) + "\t" + str(acc_by_aux[aux + '~total']) + '\n')

