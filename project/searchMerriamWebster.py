import requests
import nltk
from bs4 import BeautifulSoup
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

def searchMerriamWebster(clue, length):
    
    tokens = getSearchedTokens(clue)

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
        if len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1

    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once
    return uniqueAnswerList