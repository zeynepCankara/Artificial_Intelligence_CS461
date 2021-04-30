import nltk
import wikipedia
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

acrossClues = {"1": "Removes politely, as a hat", "2": "Rainy month", "3": "___ Tanden, Biden's pick to lead the O.M.B.", 
                    "4": "Salad green with a peppery taste", "5": 'Subject of the famous photo "The Blue Marble"'}

def searchWikipedia(clue, length):

    tokens = getSearchedTokens(clue)

    results = []

    for token in tokens:
        results = results + wikipedia.search(token)

    allAnswers = []
    lenResults = len(results)
    for i in range(lenResults):
        punctuationFree = results[i].translate(str.maketrans('', '', string.punctuation))
        possibleAnswers =  word_tokenize(punctuationFree)
        allAnswers = allAnswers + possibleAnswers

    # un-comment below line to extend the result arrays for elements with more than one words
    #allAnswers = allAnswers + results  
    
    allAnswersLength = len(allAnswers)
    i = 0
    while(allAnswersLength > i):
        if len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1
               
    return allAnswers


print("ACROSS RESULT")
for key in acrossClues:
    print(searchWikipedia(acrossClues[key], 3))
    #print()
