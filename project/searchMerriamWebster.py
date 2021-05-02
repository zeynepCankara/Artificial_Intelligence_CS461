import requests
import nltk
import json
from bs4 import BeautifulSoup
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

def iterdict(d):
    if isinstance(d, list):
        for x in d:
            iterdict(x)
    elif isinstance(d, dict):
        for v in d.values():        
            iterdict(v)
    elif isinstance(d, str):
        print(d)

def searchMerriamWebster(clue, length):
    
    tokens_and_best = getSearchedTokens(clue)
    best_token = tokens_and_best[1]
    tokens = tokens_and_best[0]

    allAnswers = []

    for token in tokens:
        webster_url = "https://dictionaryapi.com/api/v3/references/collegiate/json/" + token +"?key=28fc3ab5-65ce-49ed-8878-6b66eddf8ef5"
        thesaurus_url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/" + token + "?key=33936e00-efa4-47d5-8ef9-b897f7db33d8"
        response = json.loads(requests.get(request_url).text)
        
        iterdict(response)
        # TODO
        return

        soup = BeautifulSoup(source, 'html.parser')
        for span in soup.find_all("span", class_="ex-sent first-child t no-aq sents"):
            span.decompose()

        results = soup.find_all("span", class_="dtText")

        for result in results:
            result = result.text
            result = result[1:]
            result = result.replace("\n", "")
            result = result.replace("\t", "")
            punctuationFree = result.translate(str.maketrans('', '', string.punctuation))
            punctuationFree = punctuationFree.upper()
            allAnswers =  allAnswers + word_tokenize(punctuationFree)
    
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

searchMerriamWebster('dummy', 4)