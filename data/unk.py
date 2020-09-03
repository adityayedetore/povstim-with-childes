import re
import argparse
parser = argparse.ArgumentParser(description="unk out uncommon words")
parser.add_argument('--unk', type=str,
        help='path to file to unk')
parser.add_argument('--vocab', type=str,
        help='path to vocab eval file')
args = parser.parse_args()
def unk(filename, get_vocab_freq, cutoff = 3):
    print("====unking " + filename + "====")
    with open (get_vocab_freq, 'r') as f:
        s = f.read()

    d = {}
    for word in s.split():
        if word in d:
            d[word] += 1
        else:
            d[word] = 1

    to_unk = []
    for word in d:
        if d[word] < cutoff:
            to_unk.append(word)

    re_str = ' '.join(to_unk)
    for x in ["\\", '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')']:
        re_str = re_str.replace(x, "\\" + x)

    to_unk = re_str.split()

    print("====replacing====")
    with open(filename) as f:
        text = f.read()

    text = re.sub(' ' + ' | '.join(to_unk) + ' ', " <unk> ", text)
    text = re.sub(r'\n' + r' |\n'.join(to_unk) + ' ', "\n<unk> ", text)
    text = re.sub(' ' + r'\n| '.join(to_unk) + r'\n', " <unk>\n", text)
    print("====saving====")

    with open(filename+"~unk", 'w') as f:
        f.write(text)
unk(args.unk, args.vocab)

