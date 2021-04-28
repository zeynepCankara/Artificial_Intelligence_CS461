from parsePuzzle import parsePuzzle
from Constraints import Constraints
import copy

# TODO: Write better comments before submitting the project, my comments' purpose is explaining the code to you (Ahmet)
class State(object):
    # Make puzzleInformation and constraints static variable, since they don't change for a single puzzle (in every State, this information will be same)
    puzzleInformation = parsePuzzle(debug=True)
    constraints = Constraints(puzzleInformation)

    def __init__(self, domains = False, filledDomains = {}):
        if not domains: # Initial state, so initialize domains and shrink it with constraints
            self.domains = calculateInitialDomains(self.puzzleInformation)
            self.constraints.shrinkInitialDomains(self.domains)
        else:
            self.domains = domains
        self.filledDomains = filledDomains

    def fillDomain(self, clue, answer):
        # This function fills the cells corresponding to this clue and update domains according to the answer
        self.filledDomains[clue] = answer
        State.constraints.reduceDomainsWithAnswer(clue, answer, self.domains)

    def isStuck(self):
        # TODO: Check whether current state is stuck
        print()

    def isGoal(self):
        # TODO: Check whether current state is goal state
        print()

    def getNewState(self, clueAnswerPair):
        # This function creates a deep copy from the current state and fills a clue with the specified answer in new state. Then return this state
        clue = clueAnswerPair['clue']
        answer = clueAnswerPair['answer']

        state = copy.deepcopy(self)
        state.fillDomain(clue, answer)
        return state

    def getNextStates(self):
        # This function gets all the next states that can be reached from current state (By filling a clue with an answer from the domain)
        # and sort them according to the reduction of domain

        # What I mean is for example, if filling 1a with ahmet reduces the domain of 1d by 3 words, it is better than an answer which reduces domain of 1d by 2 words
        # (For example, if their first letters are intersecting, all words in the domain of 1d (whose first letter is not 'a') will be eliminated)
        # With this approach, we can reduce the words in domain in the best way so that search will be efficient.

        clueAnswerPairs = []
        for clue in self.domains.keys(): 
            if clue not in self.filledDomains.keys(): # Look at all unfilled clues
                for answer in self.domains[clue]: # For each answer, calculate total reduction
                    clueAnswerPairs.append({
                        'clue': clue,
                        'answer': answer,
                        'possibleDomainReduction': self.constraints.getTotalReductionForAnswer(clue, answer, self.domains)
                    })

        clueAnswerPairs.sort(reverse=True, key= lambda x: x['possibleDomainReduction']) # Sort the array with respect to total reduction (Greater is first)
        return list(map(self.getNewState, clueAnswerPairs)) #For each clue answer pair, get a new state and return the states list


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

def main():
    """Main body to run the program"""
    
    state = State()
    temp = state.getNextStates() # For debugging purposes for now
    return 0


if __name__ == "__main__":
    main()