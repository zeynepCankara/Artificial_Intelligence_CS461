def getAnswersForClue(clue, length, puzzleID):
    # TODO: Find better dummy answers for proper debugging
    # TODO: Find new dummy answer set for every puzzle (Every day I will fetch new puzzle and store it with puzzleID => look parsePuzzle.py:33)
    dummyAnswers = {
        1: {
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
        },
        2: {
            'What Calvin and Hobbes are seen riding in the final "Calvin and Hobbes" strip': ['sled'],
            'First episode of a TV show': ['pilot'],
            '"My Fair Lady" lady'       : ['eliza'],
            'Marathon handout'          : ['water'],
            '¢'                         : ['cent'],
            'Gush forth'                : ['spew'], 
            'Fragrant spring flower'    : ['lilac'],
            'Upper class'               : ['elite'],
            'Common donut order'        : ['dozen'],
            'Sour-tasting'              : ['tart']
        }
    }

    # TODO: Get possible answers with specified length for clue
    
    return dummyAnswers[puzzleID][clue]

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
    domains = {}
    for key, value in puzzleInformation['acrossClues'].items():
        domains[str(key) + 'a'] = getAnswersForClue(value, getLengthOfClueAnswer(key, True, puzzleInformation), puzzleID)
    
    for key, value in puzzleInformation['downClues'].items():
        domains[str(key) + 'd'] = getAnswersForClue(value, getLengthOfClueAnswer(key, False, puzzleInformation), puzzleID)

    return domains