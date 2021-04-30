import nltk
from nltk.corpus import wordnet   #Import wordnet from the NLTK
from createTokens import getSearchedTokens

#nltk.download('wordnet')

acrossClues = {"1": "Removes politely, as a hat", "2": "Rainy month", "3": "___ Tanden, Biden's pick to lead the O.M.B.", 
                    "4": "Salad green with a peppery taste", "5": 'Subject of the famous photo "The Blue Marble"'}

def searchWordnet(clue, length): 

    tokens = getSearchedTokens(clue)

    syn = list()
    ant = list()
    for token in tokens:
        for synset in wordnet.synsets(token):
            for lemma in synset.lemmas():
                str = lemma.name().replace("_", "")
                str = str.replace("-", "")
                syn.append(str.upper())    #add the synonyms
                if lemma.antonyms():        #When antonyms are available, add them into the list
                    str = lemma.antonyms()[0].name().replace("_", "")
                    str = str.replace("-", "")
                    ant.append(str.upper())

    allAnswers = syn + ant

    allAnswersLength = len(allAnswers)
    i = 0
    while(allAnswersLength > i):
        if len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1

    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once
    return uniqueAnswerList