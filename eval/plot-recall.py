import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Collect recall results')
parser.add_argument('--data', type=str, default='none',
        help='path to data to collect')
parser.add_argument('--out', type=str, default='results.txt', 
        help='path to out file')
parser.add_argument('--plot', type=str, default='plot-recall.png', 
        help='path to plot file')
parser.add_argument('--k', type=int, default=200,
        help='recall size')
args = parser.parse_args()


def recall_plot():
    recall= [0]*(args.k+1)
    count = 0
    with open(args.data, 'r') as f:
        for line in f:
            count +=1
            if len(line) > 5:
                recall[0] += 1
            else:
                recall[int(line)] += 1

    plt.figure(num=None, figsize=(6, 2), dpi=160)
    plt.xlabel('k')
    plt.ylabel('probability')
    recall_cdf = tuple([sum(recall[1:i])*1.0/count for i in range(1, len(recall))])
    xs = np.arange(len(recall_cdf))
    plt.bar(xs[1:51], recall_cdf[1:51], 1, align='center')

    ys = np.arange(0, 1.1, 0.2)
    plt.yticks(ys)
    plt.savefig(args.plot)
if __name__ == '__main__':
    if args.data == 'none': 
        print(parser.print_help())
    else:
        recall_plot()
