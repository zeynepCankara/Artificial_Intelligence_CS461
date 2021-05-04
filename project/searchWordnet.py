import nltk
from nltk.corpus import wordnet #Import wordnet from the NLTK
from createTokens import getSearchedTokens

#nltk.download('wordnet')

def searchWordnet(clue, length): 

    # get the tokens according to clue
    tokens_and_best = getSearchedTokens(clue)
    tokens = tokens_and_best[0]

    allAnswers = list()

    # for each token in tokens get synonyms and add them to syn
    for token in tokens:
        for synset in wordnet.synsets(token):
            for lemma in synset.lemmas():
                str = lemma.name().replace("_", "")
                str = str.replace("-", "")
                allAnswers.append(str.upper())    #add the synonyms
    

    allAnswersLength = len(allAnswers)
    i = 0
    # remove answers which do not satisfiy length constraint
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
        
    # convert list to set to remmove duplicates then conver set back to list and return list
    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once

    return uniqueAnswerList
