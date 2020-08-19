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

def ambiguous(sent, keyword="MAIN-AUX"):
    words = sent.split()
    i = words.index(keyword) + 1
    main_aux = words[i]
    return words.index(main_aux) != i

def gen(cfg_filename, output_filename): 
    with open(cfg_filename) as f:
        cfg_string = f.read()
    grammar = CFG.fromstring(cfg_string)
    gen = ""
    for sentence in generate(grammar, depth=5):
        gen += " ".join(sentence) + "\n"
    print("====done generating====")
    gen = gen[:-1]
    gen = gen.split("\n")
    gen_str = ""
    for sent in gen: 
        if (not ambiguous(sent)):
            gen_str += move(sent) + "\n"
    gen_str = gen_str[:-1]
    print("====saving " + output_filename + "====")

    with open(output_filename, "w") as f:
        f.write(gen_str)

gen("test-cfg.txt", "decl-quest-test-set.txt")
gen("gen-cfg.txt", "decl-quest-gen-set.txt")