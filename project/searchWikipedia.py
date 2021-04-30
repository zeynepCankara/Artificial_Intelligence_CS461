import nltk
import wikipedia
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

def searchWikipedia(clue, length): 

    tokens = getSearchedTokens(clue)

    results = []

    for token in tokens:
        results = results + wikipedia.search(token)

    allAnswers = []
    lenResults = len(results)
    for i in range(lenResults):
        punctuationFree = results[i].translate(str.maketrans('', '', string.punctuation))
        punctuationFree = punctuationFree.upper()
        possibleAnswers =  word_tokenize(punctuationFree)
        allAnswers = allAnswers + possibleAnswers # allAnswers (list) may includde same answer more than once

    # un-comment below line to extend the result lists for elements with more than one words
    #allAnswers = allAnswers + results  
    
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