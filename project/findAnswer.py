from getPossibleAnswers import getPossibleAnswers
from utils import log
import string
import os.path
from os import path

def getAnswersForClue(clue, length):
    log('Fetching answers for clue: ' + clue, newLine=False)

    punctuationFreeClue = clue.translate(str.maketrans('', '', string.punctuation))
    filename = punctuationFreeClue + '.txt'
    if path.exists(filename):
        f = open(filename, "r")
        possible_answers_str = f.read()
        possible_answers = possible_answers_str.split(',')
    else:
        possible_answers = getPossibleAnswers(clue, length)
        f = open(filename, "w")
        f.write(','.join(possible_answers))
        f.close()
    log('Fetched answers: ' + ', '.join(possible_answers))
    return possible_answers
    

def determineSuccessfulFetch(key, isAcross, puzzleInformation, alternatives):
    if isAcross:
        return puzzleInformation['answers'][str(key) + 'a'] in alternatives
    else:
        return puzzleInformation['answers'][str(key) + 'd'] in alternatives

def getLengthOfClueAnswer(key, isAcross, puzzleInformation):
    for i in range(0, len(puzzleInformation['cells'])):
        if puzzleInformation['cells'][i]['cellNumber'] == key:
            count = 0
            if isAcross:
                while True:
                    i = i + 1
                    count = count + 1
                    if i == 25 or puzzleInformation['cells'][i]['cellNumber'] == -1 or i % 5 == 0:
                        break
            else:
                while i < 25 and puzzleInformation['cells'][i]['cellNumber'] != -1:
                    i = i + 5
                    count = count + 1
            return count

def calculateInitialDomains(puzzleInformation):
    log('Fetching initial domains from internet')
    domains = {}
    for key, value in puzzleInformation['acrossClues'].items():
        domains[str(key) + 'a'] = {}
        domains[str(key) + 'a']['domain'] = getAnswersForClue(value, getLengthOfClueAnswer(key, True, puzzleInformation))
        domains[str(key) + 'a']['isTrue'] = determineSuccessfulFetch(key, True, puzzleInformation, domains[str(key) + 'a']['domain'])
    
    for key, value in puzzleInformation['downClues'].items():
        domains[str(key) + 'd'] = {}
        domains[str(key) + 'd']['domain'] = getAnswersForClue(value, getLengthOfClueAnswer(key, False, puzzleInformation))
        domains[str(key) + 'd']['isTrue'] = determineSuccessfulFetch(key, False, puzzleInformation, domains[str(key) + 'd']['domain'])

    log('All domains are fetched')
    return domains