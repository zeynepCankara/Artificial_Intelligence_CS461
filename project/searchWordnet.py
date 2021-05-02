import nltk
from nltk.corpus import wordnet #Import wordnet from the NLTK
from createTokens import getSearchedTokens

#nltk.download('wordnet')

def searchWordnet(clue, length): 

    tokens_and_best = getSearchedTokens(clue)
    best_token = tokens_and_best[1]
    tokens = tokens_and_best[0]

    syn = list()
    ant = list()
    hypo = list()
    hyper = list()

    for token in tokens:
        synsetlen = len(wordnet.synsets(token))
        for synset in wordnet.synsets(token):
            for lemma in synset.lemmas():
                str = lemma.name().replace("_", "")
                str = str.replace("-", "")
                syn.append(str.upper())    #add the synonyms
                if lemma.antonyms():        #When antonyms are available, add them into the list
                    str = lemma.antonyms()[0].name().replace("_", "")
                    str = str.replace("-", "")
                    ant.append(str.upper())
            
        for i in range(synsetlen):
            hyponymlen = len(wordnet.synsets(token)[i].hyponyms())
            hypernymlen = len(wordnet.synsets(token)[i].hypernyms())
            for j in range(hyponymlen):
                str = wordnet.synsets(token)[i].hyponyms()[j].name().partition(".")[0]
                str = str.replace("-", "")
                str = str.replace("_", "")
                hypo.append(str.upper())
            for j in range(hypernymlen):
                str = wordnet.synsets(token)[i].hypernyms()[j].name().partition(".")[0]
                str = str.replace("-", "")
                str = str.replace("_", "")
                hyper.append(str.upper())

    allAnswers = hyper + hypo + syn + ant
    

    allAnswersLength = len(allAnswers)
    i = 0
    while(allAnswersLength > i):
        if i+1 < allAnswersLength and len(allAnswers[i]) + len(allAnswers[i+1]) == length: # if two words can combine to create new word the combine
            allAnswers.append(allAnswers[i]+allAnswers[i+1])
            allAnswers.pop(i)
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 2
        elif len(allAnswers[i]) == length - 1 and allAnswers[i][-1] != 'S': # if does not end with s then add s
            allAnswers.append(allAnswers[i] +'S')
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        elif len(allAnswers[i]) == length + 1 and allAnswers[i][-1] == 'S': # if ends with s then remove s
            allAnswers.append(allAnswers[i][:-1])
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        elif len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1
        
    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once

    return uniqueAnswerList
