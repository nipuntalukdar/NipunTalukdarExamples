def can_conc_word(words, bigword):
    for word in words:
        if word == bigword or (bigword.startswith(word) and can_conc_word(words, bigword[len(word):])):
            return True
    return False

def con_words(lst):
    sizes = []
    size_words = {}
    for word in lst:
        if len(word) not in size_words:
            size_words[len(word)] = [word]
            sizes.append(len(word))
        else:
            size_words[len(word)].append(word)
    for i in range(1,len(sizes)):
        words = []
        for j in range(i):
            words += size_words[sizes[j]]
        for bigword in size_words[sizes[i]]:
            if can_conc_word(words, bigword):
                print(bigword)



con_words(["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"])
