# Code taken from https://eli.thegreenplace.net/2010/01/28/generating-random-sentences-from-a-context-free-grammar
# All code in the public domain

from collections import defaultdict
import random
import sys
import argparse

parser = argparse.ArgumentParser(description="Generate random sentences from CFG")
parser.add_argument('--n', type=int, default=10000,
        help='number of sentences to generate')
args=parser.parse_args()

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)
    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))
    def gen_random(self, symbol):
        sentence = ""
        rand_prod = random.choice(self.prod[symbol])
        for sym in rand_prod:
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' ' 
        return sentence 

def move(sent, keyword="MAIN-AUX"):
    decl = sent.split()
    decl.pop(decl.index(keyword))
    quest = sent.split()
    i = quest.index(keyword)
    quest.insert(0, quest.pop(i + 1))
    quest.pop(i + 1)
    return ' '.join(decl) + " . " + ' '.join(quest) + " ?"

def ambiguous(sent, keyword="MAIN-AUX"):
    words = sent.split()
    i = words.index(keyword) + 1
    main_aux = words[i]
    return words.index(main_aux) != i

def gen(cfg, vocab, output, n=10000):
    grammar = CFG()
    print("reading from " + cfg + " and printing to " + output)
    print("====generating====")
    with open(cfg, 'r') as f:
        cfg_rules = f.readlines()
    for rule in cfg_rules:
        if rule.strip():
            lhs = rule.split("->")[0].strip()
            rhs = rule.split("->")[1]
            grammar.add_prod(lhs, rhs)
    with open(vocab, 'r') as f:
        cfg_rules = f.readlines()
    for rule in cfg_rules:
        if rule.strip():
            lhs = rule.split("->")[0].strip()
            rhs = rule.split("->")[1]
            grammar.add_prod(lhs, rhs)
    with open(output, 'w') as f:
        while n > 0:
            sent = grammar.gen_random('S')
            if not ambiguous(sent):
                msent = move(sent) + "\n"
                f.write(msent.replace("-", " "))
                n -= 1


if __name__ == "__main__":
    gen(cfg="test-cfg.txt", vocab="vocab-cfg.txt", output="decl-quest-test-set.txt", n=args.n)
    gen(cfg="gen-cfg.txt", vocab="vocab-cfg.txt", output="decl-quest-gen-set.txt", n=args.n)
