import pandas as pd
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="summarize breakdown data")

parser.add_argument('--data', nargs='+', required=True, 
        help='<Required> list of data to summarize')
parser.add_argument('--out', type=str, default='output.txt', 
        help='path to output file')
parser.add_argument('--test', type=str, default='test', 
        help='use valid if training')
parser.add_argument('--gen', type=str, default='gen', 
        help='use test if training')

args = parser.parse_args()


index = list(set(''.join(i for i in f if i.isdigit()) for f in args.data))
columns=['seed',args.test + ' full accuracy',args.test + ' first word accuracy',args.gen + ' full accuracy',args.gen + ' move first',args.gen + ' move main']
df_out = pd.DataFrame(index=index, columns=columns)
for f in args.data:
    print(f)
    seed = ''.join(i for i in f if i.isdigit())
    df = pd.read_csv(f)
    df_out['seed'][seed] = ''.join(j for j in f if j.isdigit())
    if args.test in f:
        l = len(df['target'])
        df_out[args.test + ' full accuracy'][seed] = sum(int(df['target'][k]==df['actual'][k]) for k in range(0, l))/l
        df_out[args.test + ' first word accuracy'][seed] = sum(df['move_main_aux'])/l
    if args.gen in f:
        l = len(df['target'])
        df_out[args.gen + ' full accuracy'][seed] = sum(int(df['target'][k]==df['actual'][k]) for k in range(0, l))/l
        df_out[args.gen + ' move first'][seed] = sum(df['move_first_aux'])/l
        df_out[args.gen + ' move main'][seed] = sum(df['move_main_aux'])/l
df_out.to_csv(args.out, index=False)

names = []
values = []
for col in df_out.columns:
    if 'seed' not in col:
        names.append(col)
        values.append(sum(df_out[col])/len(df_out[col]))
        print(col, values[-1])
plt.barh(names, values)
plt.xlim((0,1.05))
plt.savefig("barh-plot.png", bbox_inches='tight')
plt.clf()
names = []
values = []
for col in df_out.columns:
    for x in df_out[col]:
        names.append(col)
        values.append(x)
#plt.ylim((0,1))
#i = values.index(args.test + 
#plt.scatter(names[i:], values[i:])
#plt.savefig("scatter-plot.png", bbox_inches='tight')

