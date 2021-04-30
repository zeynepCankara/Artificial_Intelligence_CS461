from getPossibleAnswers import getPossibleAnswers

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

    # TODO: Get possible answers with specified length for clue
    #getPossibleAnswers(clue, length)
    
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