from parsePuzzle import parsePuzzle
from Constraints import Constraints
from findAnswer import calculateInitialDomains
from collections import OrderedDict
import copy
from puzzleID import puzzleID
from utils import log, getClueFromShortVersion

# TODO: Write better comments before submitting the project, my comments' purpose is explaining the code to you (Ahmet)
class State(object):
    # Make puzzleInformation and constraints static variable, since they don't change for a single puzzle (in every State, this information will be same)
    puzzleInformation = parsePuzzle(puzzleID)

    def __init__(self, domains = False, filledDomains = OrderedDict()):
        if not domains: # Initial state, so initialize domains and shrink it with constraints
            domains = calculateInitialDomains(self.puzzleInformation, puzzleID)
            self.domains = {}
            self.found = {}
            for k, v in domains.items():
                self.domains[k] = v['domain']
                self.found[k] = v['isTrue']
            self.constraints = Constraints(self.puzzleInformation)
            self.constraints.shrinkInitialDomains(self.domains, self.puzzleInformation['answers'])
            for shortVersion, domain in self.domains.items():
                log(getClueFromShortVersion(shortVersion, self.puzzleInformation) + ' -> ' + ', '.join(domain), newLine=False)
            print()
        else:
            self.domains = domains
        self.lastAnswer = ()
        self.filledDomains = filledDomains

    def __eq__(self, other):
        # For 'in' operation to work correctly, we must implement a custom equality operator
        return self.domains == other.domains and self.filledDomains == other.filledDomains
    
    def __repr__(self):
        # In the debug panel, states can be visualized better if we represent them by their filledDomains
        return str(self.filledDomains)

    def __hash__(self):
        # To add a State object to a set, we must implement a hash function
        return hash(str((self.domains, self.filledDomains)))

    def fillDomain(self, clue, answer):
        # This function fills the cells corresponding to this clue and update domains according to the answer
        self.filledDomains[clue] = answer
        if answer == '':
            self.constraints.removeConstraintsForClue(clue)
        else:
            self.constraints.reduceDomainsWithAnswer(clue, answer, self.domains)
        # State.constraints.reduceDomainsWithAnswer(clue, answer, self.domains)
        self.lastAnswer = (clue, answer)

    def isStuck(self):
        # if self.lastAnswer != () and self.lastAnswer[1] == '' and self.found[self.lastAnswer[0]]:
        #     return True

        if self.isGoal(): # If it is goal state, return False immediately
            return False

        for clue, answer in State.puzzleInformation['answers'].items():
            if clue not in self.filledDomains.keys(): # There is a clue which is not answered yet, so state is not stucked
                return False

        # All clues are answered since all of them are present in filledDomains. However, it is not goal state because of the initial check in this function
        # So, this state is definitely stuck
        return True

    def isGoal(self):
        isGoal = True
        for clue, answer in State.puzzleInformation['answers'].items():
            if clue not in self.filledDomains.keys() or (self.filledDomains[clue] != '' and self.filledDomains[clue] != answer):
                isGoal = False
                break
        return isGoal

    def getNewState(self, clueAnswerPair):
        # This function creates a deep copy from the current state and fills a clue with the specified answer in new state. Then return this state
        clue = clueAnswerPair['clue']
        answer = clueAnswerPair['answer']

        state = copy.deepcopy(self)
        state.fillDomain(clue, answer)
        return state

    def getNextStates(self):
        # This function first gets clue with smallest possible answers in its domain and sorts the answers according to the reduction they provide

        # What I mean is for example, if filling 1a with ahmet reduces the domain of 1d by 3 words, it is better than an answer which reduces domain of 1d by 2 words
        # (For example, if their first letters are intersecting, all words in the domain of 1d (whose first letter is not 'a') will be eliminated)
        # With this approach, we can reduce the words in domain in the best way so that search will be efficient.

        unfilledClues = list(filter(lambda x: x not in self.filledDomains.keys(), self.domains.keys()))
        clue = min(unfilledClues, key = lambda x: len(self.domains[x]))

        clueAnswerPairs = []
        for answer in self.domains[clue]: # For each answer, calculate total reduction
            clueAnswerPairs.append({
                'clue': clue,
                'answer': answer,
                'possibleDomainReduction': self.constraints.getTotalReductionForAnswer(clue, answer, self.domains, self.filledDomains)
            })

        clueAnswerPairs = list(filter(lambda x: x['possibleDomainReduction'] != -1,clueAnswerPairs)) # Eliminate impossible clue answer pairs (which will eliminate all possible answers for another domain)
        clueAnswerPairs.sort(key= lambda x: x['possibleDomainReduction']) # Sort the array with respect to total reduction
        clueAnswerPairs.insert(0, {
                'clue': clue,
                'answer': ''
        })
        return list(map(self.getNewState, clueAnswerPairs)) #For each clue answer pair, get a new state and return the states list