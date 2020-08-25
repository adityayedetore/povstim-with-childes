from nltk.parse.generate import generate
from nltk import CFG
import os

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

def gen(cfg, vocab="vocab-cfg.txt", output="output.txt"): 
    print("reading from " + cfg + " and printing to " + output)
    print("====generating====")
    with open(cfg) as f:
        cfg_string = f.read() + "\n"
    with open (vocab) as f:
        cfg_string += f.read()
    grammar = CFG.fromstring(cfg_string)
    gen = ""
    count = 0
    for sentence in generate(grammar, depth=5):
        if count % 100000 == 0:
            print(str(count) + " done")
        gen += " ".join(sentence) + "\n"
    print("====moving====")
    gen = gen[:-1]
    gen = gen.split("\n")
    gen_str = ""
    count = 0
    with open(output, "w") as f:
        for sent in gen: 
            if count % 100000 == 0:
                print(str(count) + " done")
                f.write(gen_str[count:])
            if (not ambiguous(sent)):
                gen_str += move(sent) + "\n"
        gen_str = gen_str[:-1]
    print("====saving to " + output + "====")

    with open(output, "w") as f:
        f.write(gen_str[count:])

gen("test-cfg.txt", vocab="vocab-cfg.txt", output="decl-quest-test-set.txt~medium")
gen("gen-cfg.txt", vocab="vocab-cfg.txt", output="decl-quest-gen-set.txt~medium")
