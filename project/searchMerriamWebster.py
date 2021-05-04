import requests
import nltk
import json
import re
import string
from createTokens import getSearchedTokens
from nltk.tokenize import word_tokenize

#Parser for Webster URL response
def iter_webster(d):
    answers = []
    if not isinstance(d, list):
        return answers
    for x in d:
        if isinstance(x, str):
            answers.append(x)
        else:
            answers = answers + x['shortdef']
    return answers

#Parser for Thesaurus URL response
def iter_thesaurus(d):
    answers = []
    if not isinstance(d, list):
        return answers
    for x in d:
        if isinstance(x, str):
            answers.append(x)
        else:
            for syn in x['meta']['syns']:
                answers = answers + syn
            for ant in x['meta']['ants']:
                answers = answers + ant
    return answers

def searchMerriamWebster(clue, length):
    
    #Get the tokens for the specified clue
    tokens_and_best = getSearchedTokens(clue)
    tokens = tokens_and_best[0]

    webster = []
    thesaurus = []
    results = []
    allAnswers = []

    for token in tokens:
        webster_url = "http://dictionaryapi.com/api/v3/references/collegiate/json/" + token +"?key=28fc3ab5-65ce-49ed-8878-6b66eddf8ef5"
        thesaurus_url = "http://dictionaryapi.com/api/v3/references/thesaurus/json/" + token + "?key=33936e00-efa4-47d5-8ef9-b897f7db33d8"
        
        response = json.loads(requests.get(thesaurus_url).text) #loading the content of the Thesaurus webpage
        thesaurus = iter_thesaurus(response)

        response = json.loads(requests.get(webster_url).text) #loading the content of the Collegiate webpage
        webster = iter_webster(response)

        results = thesaurus + webster #Merging the results of the Saurus and dictionary parts

        #Unnecessary chars and strings are removed from the results and then tokenize each result in the results list.
        for result in results:
            result = re.sub(r'{\w+}|[^a-zA-Z]', '', result)
            result = result.replace("\n", " ")
            result = result.replace("\t", " ")
            result = result.replace("_", "")
            result = result.replace("-", "")
            punctuationFree = result.translate(str.maketrans('', '', string.punctuation))
            punctuationFree = punctuationFree.upper()
            allAnswers =  allAnswers + word_tokenize(punctuationFree)

    allAnswersLength = len(allAnswers)
    i = 0
    #Remove answers which do not satisfy length constraint and checking other syntax constraints
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
        elif len(allAnswers[i]) == length + 1 and allAnswers[i][-2:] == 'ED': # if ends with d then remove d
            allAnswers.append(allAnswers[i][:-1])
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        elif len(allAnswers[i]) != length:
            allAnswers.pop(i)
            i = i - 1
            allAnswersLength = allAnswersLength - 1
        i = i + 1

     #Convert list to set to remove duplicates then conver set back to list and return list
    uniqueAnswers = set(allAnswers)
    uniqueAnswerList = list(uniqueAnswers)  #uniqueAnswerList contains each answer only once
    return uniqueAnswerList
