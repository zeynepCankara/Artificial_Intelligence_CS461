def getAnswersForClue(clue, length):
    # TODO: Find better dummy answers for proper debugging
    dummyAnswers = {
    'Test of responsibility before a pet or kid':       ['plant', 'pants', 'shity', 'water'],
    'Word before student or system ':                   ['honor', 'ahmet', 'memet'],
    'First line on the phone to someone you know well': ['itsme', 'kitty', 'pitty'],
    'Rare order at a restaurant':                       ['steak', 'forty'],
    'Waits on the phone':                               ['holds', 'hodor', 'hello'],
    'Jam band fronted by guitarist Trey Anastasio':     ['phish', 'ssshh', 'papfh'],
    'Scratch-off ticket game':                          ['lotto', 'cozyy', 'proud', 'ahioo'],
    '"Moon And Half Dome" photographer Adams':          ['ansel', 'fancy', 'nmtrd'],
    'Wanderer':                                         ['nomad', 'pomad', 'comar', 'tetto'],
    'Arduous journeys':                                 ['treks', 'shrek', 'melek', 'styyr']
    }

    # TODO: Get possible answers with specified length for clue
    
    return dummyAnswers[clue]

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
    domains = {}
    for key, value in puzzleInformation['acrossClues'].items():
        domains[str(key) + 'a'] = getAnswersForClue(value, getLengthOfClueAnswer(key, True, puzzleInformation))
    
    for key, value in puzzleInformation['downClues'].items():
        domains[str(key) + 'd'] = getAnswersForClue(value, getLengthOfClueAnswer(key, False, puzzleInformation))

    return domains