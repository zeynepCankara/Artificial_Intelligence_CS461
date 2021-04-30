import requests
import nltk
from bs4 import BeautifulSoup
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

acrossClues = {"1": "Removes politely, as a hat", "2": "Rainy month", "3": "___ Tanden, Biden's pick to lead the O.M.B.", 
                    "4": "Salad green with a peppery taste", "5": 'Subject of the famous photo "The Blue Marble"'}

URL = "https://www.merriam-webster.com/dictionary/"


def searchMerriamWebster(clue, length):
    
    tokens = getSearchedTokens(clue)

    words = []

    for token in tokens:
        request_url = URL + token
        page = requests.get(request_url)
        source = page.text
        soup = BeautifulSoup(source, 'html.parser')
        for span in soup.find_all("span", class_="ex-sent first-child t no-aq sents"):
            span.decompose()

        result_list = soup.find_all("span", class_="dtText")

        for result in result_list:
            result = result.text
            result = result[1:]
            result = result.replace("\n", "")
            result = result.replace("\t", "")
            punctuationFree = result.translate(str.maketrans('', '', string.punctuation))
            words =  words + word_tokenize(punctuationFree)
    
    allAnswersLength = len(words)
    i = 0
    while(allAnswersLength > i):
        if len(words[i]) != length:
            words.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1
               
    return words


print("ACROSS RESULT")
for key in acrossClues:
    print(searchMerriamWebster(acrossClues[key], 3))
