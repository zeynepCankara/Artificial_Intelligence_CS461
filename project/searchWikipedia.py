import nltk
import wikipedia
import string
import re
import warnings
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

warnings.catch_warnings()
warnings.simplefilter("ignore")

def searchWikipedia(clue, length): 

    #Get the tokens for the specified clue
    tokens_and_best = getSearchedTokens(clue)
    best_token = tokens_and_best[1]
    tokens = tokens_and_best[0]

    results = []

    """ Searching wikipedia by using library for each token in
        the clue and add the result to results list. Try to get
        the matched page with the specified token.
    """
    for token in tokens:
        search_results = wikipedia.search(token)
        results = results + search_results
        if token == best_token:
            best_result = search_results[0]

    #Regulating the results obtained from the webpage and tokenize them
    try:
        page = wikipedia.page(best_result)
        content = page.content
        words = word_tokenize(content)
        results.extend(words)
    except:
        print("Page not found in wiki!\n")

    #Unnecessary chars and strings are removed from the results and then tokenize each result in the results list.
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
 
    
    #Applying the length constraint to the each word
    allAnswersLength = len(allAnswers)
    i = 0
    while(allAnswersLength > i):
        if len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1

    #Convert list to set to remove duplicates then conver set back to list and return list    
    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once
    return uniqueAnswerList