from getPossibleAnswers import getPossibleAnswers
from utils import log
import string
import os.path
from os import path

def getAnswersForClue(clue, length, puzzleID):
    # TODO: Find better dummy answers for proper debugging
    # TODO: Find new dummy answer set for every puzzle (Every day I will fetch new puzzle and store it with puzzleID => look parsePuzzle.py:33)
    dummyAnswers = {
        1: {
            'Test of responsibility before a pet or kid':       ['PLANT', 'PANTS', 'SHITY', 'WATER'],
            'Word before student or system ':                   ['HONOR', 'AHMET', 'MEMET'],
            'First line on the phone to someone you know well': ['ITSME', 'KITTY', 'PITTY'],
            'Rare order at a restaurant':                       ['STEAK', 'FORTY'],
            'Waits on the phone':                               ['HOLDS', 'HODOR', 'HELLO'],
            'Jam band fronted by guitarist Trey Anastasio':     ['PHISH', 'SSSHH', 'PAPFH'],
            'Scratch-off ticket game':                          ['LOTTO', 'COZYY', 'PROUD', 'AHIOO'],
            '"Moon And Half Dome" photographer Adams':          ['ANSEL', 'FANCY', 'NMTRD'],
            'Wanderer':                                         ['NOMAD', 'POMAD', 'COMAR', 'TETTO'],
            'Arduous journeys':                                 ['TREKS', 'SHREK', 'MELEK', 'STYYR']
        },
        2: {
            'What Calvin and Hobbes are seen riding in the final "Calvin and Hobbes" strip': ['SLED'],
            'First episode of a TV show': ['PILOT'],
            '"My Fair Lady" lady'       : ['ELIZA'],
            'Marathon handout'          : ['WATER'],
            '¢'                         : ['CENT'],
            'Gush forth'                : ['SPEW'], 
            'Fragrant spring flower'    : ['LILAC'],
            'Upper class'               : ['ELITE'],
            'Common donut order'        : ['DOZEN'],
            'Sour-tasting'              : ['TART']
        },
        3: {
            'Web page … and a homophone of 1- and 5-Down'   : ['SITE'],
            'Polite'                                        : ['CIVIL'],
            '"O.K., you win"'                               : ['IGIVE'],
            '2000s Fox drama set in Newport Beach'          : ['THEOC'],
            'Aliens, for short'                             : ['ETS'],
            'One of the senses'                             : ['SIGHT'],
            'Wall-climbing plants'                          : ['IVIES'],
            'Save for later viewing'                        : ['TIVO'],
            'Monthly utility bill: Abbr.'                   : ['ELEC'],
            'Credit in a footnote'                          : ['CITE']
        }
    }

    # return dummyAnswers[puzzleID][clue]

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

def calculateInitialDomains(puzzleInformation, puzzleID):
    log('Fetching initial domains from internet')
    domains = {}
    for key, value in puzzleInformation['acrossClues'].items():
        domains[str(key) + 'a'] = {}
        domains[str(key) + 'a']['domain'] = getAnswersForClue(value, getLengthOfClueAnswer(key, True, puzzleInformation), puzzleID)
        domains[str(key) + 'a']['isTrue'] = determineSuccessfulFetch(key, True, puzzleInformation, domains[str(key) + 'a']['domain'])
    
    for key, value in puzzleInformation['downClues'].items():
        domains[str(key) + 'd'] = {}
        domains[str(key) + 'd']['domain'] = getAnswersForClue(value, getLengthOfClueAnswer(key, False, puzzleInformation), puzzleID)
        domains[str(key) + 'd']['isTrue'] = determineSuccessfulFetch(key, False, puzzleInformation, domains[str(key) + 'd']['domain'])

    log('All domains are fetched')
    return domains