import requests
import nltk
from bs4 import BeautifulSoup
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

def searchMerriamWebster(clue, length):
    
    tokens_and_best = getSearchedTokens(clue)
    best_token = tokens_and_best[1]
    tokens = tokens_and_best[0]

    allAnswers = []

    for token in tokens:
        request_url = "https://www.merriam-webster.com/dictionary/" + token
        page = requests.get(request_url)
        source = page.text
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