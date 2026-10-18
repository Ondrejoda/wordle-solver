words = []

global_probs = {'A': 0.4220103986135182, 'B': 0.12131715771230503, 'C': 0.20580589254766032, 'D': 0.17027729636048528, 'E': 0.5324956672443674, 'F': 0.09878682842287695, 'G': 0.134315424610052, 'H': 0.16767764298093588, 'I': 0.2902946273830156, 'J': 0.01169844020797227, 'K': 0.09098786828422877, 'L': 0.30979202772963604, 'M': 0.1369150779896014, 'N': 0.24826689774696706, 'O': 0.3262564991334489, 'P': 0.15814558058925476, 'Q': 0.012564991334488735, 'R': 0.3886481802426343, 'S': 0.2889948006932409, 'T': 0.3158578856152513, 'U': 0.2019064124783362, 'V': 0.0658578856152513, 'W': 0.08405545927209705, 'X': 0.016031195840554593, 'Y': 0.18370883882149047, 'Z': 0.01733102253032929}

def evaluate_word(word, probs):
    evaled = []
    rtn = 0
    for letter in word:
        if not letter in evaled:
            rtn += probs[letter]
        evaled.append(letter)
    return rtn

def get_best_word(words, probs):
    best_word = words[0]
    best_eval = evaluate_word(best_word, probs)
    for word in words:
        eval = evaluate_word(word, probs)
        if eval > best_eval:
            best_word = word
            best_eval = eval
    return (best_word, best_eval)

def reevaluate_probs(words):
    probs = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.0, 'F': 0.0, 'G': 0.0, 'H': 0.0, 'I': 0.0, 'J': 0.0, 'K': 0.0, 'L': 0.0, 'M': 0.0, 'N': 0.0, 'O': 0.0, 'P': 0.0, 'Q': 0.0, 'R': 0.0, 'S': 0.0, 'T': 0.0, 'U': 0.0, 'V': 0.0, 'W': 0.0, 'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    for word in words:
        for letter in word:
            probs[letter] = probs[letter] + 1.0

    for key in probs.keys():
        probs[key] = probs[key] / len(words)
    return probs

def get_possible_words(greens, yellows, greys):
    global words, probs
    rtn = []
    for word in words:
        con = False

        for i in range(len(greens)):
            if not greens[i] == word[i] and greens[i] != "":
                con = True
                break
        if con: continue

        for yellow_row in yellows:
            for i in range(len(yellow_row)):
                yellow = yellow_row[i]
                if yellow == "":
                    continue

                if not yellow in word or yellow == word[i]:
                    con = True
            if con: break
        if con: continue

        for grey in greys:
            if grey in word and not grey == "" and grey not in greens:
                is_in_yellow = False
                for yellow_row in yellows:
                    if grey in yellow_row:
                        is_in_yellow = True
                if not is_in_yellow:
                    con = True
                    break

        if con: continue
        rtn.append(word)
    return rtn

with open("words.csv", "r") as file:
    for line in file:
        word = line.strip("\n").upper()
        words.append(word)

greens = ["", "", "", "", ""]
yellows = []
greys = []
probs = global_probs

while True:
    possible_words = get_possible_words(greens, yellows, greys)
    print("words remaining:", len(possible_words))
    if len(possible_words) == 0:
        print("no words left")
        break
    if len(possible_words) <= 10:
        print("candidates:", possible_words)
    probs = reevaluate_probs(possible_words)
    local_eval = get_best_word(possible_words, probs)
    print("best:", local_eval[0], "eval:", local_eval[1])

    ipt = input(": ").upper()

    yellow_row = ["", "", "", "", ""]
    for h in range(5):
        letter = ipt[h * 2]
        command = ipt[h * 2 + 1]
        match command:
            case "/":
                greens[h] = letter
            case ",":
                yellow_row[h] = letter
            case ".":
                greys.append(letter)
            case _:
                pass
    
    yellows.append(yellow_row)
      