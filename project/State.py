from parsePuzzle import parsePuzzle

class State(object):
    def __init__(self, domains, puzzleInformation, filledDomains, debug = False):
        
        self.puzzleInformation = puzzleInformation
        self.domains = domains
        self.filledDomains = filledDomains

    def shrinkDomains(self):
        for acrossKey in self.puzzleInformation['acrossClues'].keys():
            for i in range(0, len(self.puzzleInformation['cells'])):
                if self.puzzleInformation['cells'][i]['cellNumber'] == acrossKey:
                    acrossIndex = 0
                    while True:
                        self.findDownClueMatch(i, acrossKey, acrossIndex)
                        i = i + 1
                        acrossIndex = acrossIndex + 1
                        if i == 25 or self.puzzleInformation['cells'][i]['cellNumber'] == -1 or i % 5 == 0:
                            break
                    break

    def findDownClueMatch(self, i, acrossKey, acrossIndex):
        for downKey in self.puzzleInformation['downClues'].keys():
            for j in range(0, len(self.puzzleInformation['cells'])):
                if self.puzzleInformation['cells'][j]['cellNumber'] == downKey:
                    downIndex = 0
                    while j < 25 and self.puzzleInformation['cells'][j]['cellNumber'] != -1:
                        if i == j:
                            self.checkConstraint(str(acrossKey) + 'a', str(downKey) + 'd', acrossIndex, downIndex)
                            return
                        j = j + 5
                        downIndex = downIndex + 1
                    break    

    def checkConstraint(self, across, down, acrossIndex, downIndex):
        print('Across:', across, 'Down:', down, 'AcrossIndex:', acrossIndex, 'DownIndex:', downIndex)
        acrossChars = list(map(lambda x: x[acrossIndex], self.domains[across]))
        downChars =  list(map(lambda x: x[downIndex], self.domains[down]))
        
        i = 0
        while i < len(self.domains[across]):
            if self.domains[across][i][acrossIndex] not in downChars:
                self.domains[across].remove(self.domains[across][i])
            else:
                i = i + 1
            
        i = 0
        while i < len(self.domains[down]):
            if self.domains[down][i][downIndex] not in acrossChars:
                self.domains[down].remove(self.domains[down][i])
            else:
                i = i + 1

    def fillDomain(self, domain, answer):
        # TODO: Remove answers other that this answer from specified domain, add domain to filledDomains. Lastly, call shrinkDomains method
        print()

    def isStuck(self):
        # TODO: Check whether current state is stuck
        print()

    def isGoal(self):
        # TODO: Check whether current state is goal state
        print()

    def getNextState(self):
        # TODO: Look at domains, and select the domain with lowest number of possible answers.
        # After, construct new state by inserting random answer to that position and return it.

        domain = '1a'
        answer = 'plant'

        state = State(self.domains, self.puzzleInformation, True)
        state.fillDomain(domain, answer)

        return state


def getAnswersForClue(clue, length):
    # TODO: Find better dummy answers for proper debugging
    dummyAnswers = {
    'Test of responsibility before a pet or kid':       ['plant', 'pants', 'shity', 'water'],
    'Word before student or system ':                   ['honor', 'ahmet', 'memet'],
    'First line on the phone to someone you know well': ['itsme', 'kitty', 'pitty'],
    'Rare order at a restaurant':                       ['steak', 'forty'],
    'Waits on the phone':                               ['holds', 'hodor', 'hello'],
    'Jam band fronted by guitarist Trey Anastasio':     ['phish', 'ssshh'],
    'Scratch-off ticket game':                          ['lotto', 'cozyy', 'proud'],
    '"Moon And Half Dome" photographer Adams':          ['ansel', 'fancy'],
    'Wanderer':                                         ['nomad', 'pomad', 'comar'],
    'Arduous journeys':                                 ['treks', 'shrek', 'melek']
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

def calculateDomains(puzzleInformation):
    domains = {}
    for key, value in puzzleInformation['acrossClues'].items():
        domains[str(key) + 'a'] = getAnswersForClue(value, getLengthOfClueAnswer(key, True, puzzleInformation))
    
    for key, value in puzzleInformation['downClues'].items():
        domains[str(key) + 'd'] = getAnswersForClue(value, getLengthOfClueAnswer(key, False, puzzleInformation))

    return domains

def constructInitialState(debug = False):
    if debug:
        puzzleInformation = {
            'cells': [{'cellNumber': 1, 'letter': 'P'}, {'cellNumber': 2, 'letter': 'L'}, {'cellNumber': 3, 'letter': 'A'}, {'cellNumber': 4, 'letter': 'N'}, {'cellNumber': 5, 'letter': 'T'}, 
                        {'cellNumber': 6, 'letter': 'H'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'N'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'R'}, 
                        {'cellNumber': 7, 'letter': 'I'}, {'cellNumber': 0, 'letter': 'T'}, {'cellNumber': 0, 'letter': 'S'}, {'cellNumber': 0, 'letter': 'M'}, {'cellNumber': 0, 'letter': 'E'},
                        {'cellNumber': 8, 'letter': 'S'}, {'cellNumber': 0, 'letter': 'T'}, {'cellNumber': 0, 'letter': 'E'}, {'cellNumber': 0, 'letter': 'A'}, {'cellNumber': 0, 'letter': 'K'},
                        {'cellNumber': 9, 'letter': 'H'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'L'}, {'cellNumber': 0, 'letter': 'D'}, {'cellNumber': 0, 'letter': 'S'}],
            'acrossClues': {1: 'Test of responsibility before a pet or kid', 6: 'Word before student or system ', 7: 'First line on the phone to someone you know well', 8: 'Rare order at a restaurant', 9: 'Waits on the phone'},
            'downClues': {1: 'Jam band fronted by guitarist Trey Anastasio', 2: 'Scratch-off ticket game', 3: '"Moon And Half Dome" photographer Adams', 4: 'Wanderer', 5: 'Arduous journeys'}
            }
    else:
        puzzleInformation = parsePuzzle()

    state = State(calculateDomains(puzzleInformation), puzzleInformation, debug)
    state.shrinkDomains()

    return state

def main():
    """Main body to run the program"""

    state = constructInitialState(True)

    return 0


if __name__ == "__main__":
    main()