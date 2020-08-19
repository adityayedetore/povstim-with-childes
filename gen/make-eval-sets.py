from nltk.parse.generate import generate
from nltk import CFG

def move(sent, keyword="MAIN-AUX"):
    decl = sent.split()
    decl.pop(decl.index(keyword))
    quest = sent.split()
    i = quest.index(keyword)
    quest.insert(0, quest.pop(i + 1))
    quest.pop(i + 1)
    return ' '.join(decl) + " . " + ' '.join(quest) + " ?"

def gen(): 
    with open('cfg.txt') as f:
        cfg_string = f.read()

    grammar = CFG.fromstring(cfg_string)

    gen = ""
    for sentence in generate(grammar):
        gen += " ".join(sentence) + "\n"
    gen = gen[:-1]

    gen = gen.split("\n")

    
    gen_str = ""
    for sent in gen: 
        gen_str += move(sent) + "\n"
    gen_str = gen_str[:-1]

    print("====saving decl-quest-gen.txt====")

    with open("gen-set.txt", "w") as f:
        f.write(gen_str)
gen()
