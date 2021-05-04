import nltk
import wikipedia
import string
import re
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

def searchWikipedia(clue, length): 

    tokens_and_best = getSearchedTokens(clue)
    best_token = tokens_and_best[1]
    tokens = tokens_and_best[0]

    results = []

    for token in tokens:
        search_results = wikipedia.search(token)
        results = results + search_results
        if token == best_token:
            best_result = search_results[0]

    try:
        page = wikipedia.page(best_result)
        content = page.content
        words = word_tokenize(content)
        results.extend(words)
    except:
        print("Page not found in wiki!\n")


    allAnswers = []
    lenResults = len(results)
    for i in range(lenResults):
        results[i] = re.sub(r'[0-9]+|[^a-zA-Z ]', '', results[i])
        results[i].replace("_", "")
        results[i].replace("-", "")
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