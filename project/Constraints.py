from utils import log

# TODO: Add comments
class Constraint(object):
    def __init__(self, acrossClue, acrosIndex, downClue, downIndex):
        self.acrossClue = acrossClue
        self.acrossIndex = acrosIndex
        self.downClue = downClue
        self.downIndex = downIndex
    
    def getReductionCountForAnswer(self, clue, answer, domains, filledDomains):
        count = 0
        if clue == self.acrossClue and self.downClue not in filledDomains.keys():
            downChars =  list(map(lambda x: x[self.downIndex], domains[self.downClue]))
            for char in downChars:
                if answer[self.acrossIndex] != char:
                    count = count + 1
        elif clue == self.downClue and self.acrossClue not in filledDomains.keys():
            acrossChars = list(map(lambda x: x[self.acrossIndex], domains[self.acrossClue]))
            for char in acrossChars:
                if answer[self.downIndex] != char:
                    count = count + 1
        
        return count

    def applyConstraint(self, clue, answer, domains):
        i = 0
        if clue == self.acrossClue:
            while i < len(domains[self.downClue]):
                if answer[self.acrossIndex] != domains[self.downClue][i][self.downIndex]:
                    domains[self.downClue].remove(domains[self.downClue][i])
                else:
                    i = i + 1
        else:
            while i < len(domains[self.acrossClue]):
                if answer[self.downIndex] != domains[self.acrossClue][i][self.acrossIndex]:
                    domains[self.acrossClue].remove(domains[self.acrossClue][i])
                else:
                    i = i + 1

class Constraints(object):
    def __init__(self, puzzleInformation):
        self.constraints = self.generateConstraints(puzzleInformation)
    
    def generateConstraints(self, puzzleInformation):
        log('Generating constraints according to puzzle information')
        result = []
        for acrossKey in puzzleInformation['acrossClues'].keys():
            for i in range(0, len(puzzleInformation['cells'])):
                if puzzleInformation['cells'][i]['cellNumber'] == acrossKey:
                    acrossIndex = 0
                    while True:
                        result.append(self.findDownClueMatch(puzzleInformation, i, acrossKey, acrossIndex))
                        i = i + 1
                        acrossIndex = acrossIndex + 1
                        if i == 25 or puzzleInformation['cells'][i]['cellNumber'] == -1 or i % 5 == 0:
                            break
                    break
        return result

    def findDownClueMatch(self, puzzleInformation, i, acrossKey, acrossIndex):
        for downKey in puzzleInformation['downClues'].keys():
            for j in range(0, len(puzzleInformation['cells'])):
                if puzzleInformation['cells'][j]['cellNumber'] == downKey:
                    downIndex = 0
                    while j < 25 and puzzleInformation['cells'][j]['cellNumber'] != -1:
                        if i == j:
                            return Constraint(str(acrossKey) + 'a', acrossIndex, str(downKey) + 'd', downIndex)
                        j = j + 5
                        downIndex = downIndex + 1
                    break 
    
    def findConstraintsForClue(self, clue):
        result = []
        if 'a' in clue:
            result = filter(lambda constraint: constraint.acrossClue == clue, self.constraints)
        else:
            result = filter(lambda constraint: constraint.downClue == clue, self.constraints)   
        return list(result)

    def getTotalReductionForAnswer(self, clue, answer, domains, filledDomains):
        total = 0
        for constraint in self.findConstraintsForClue(clue):
            reduction = constraint.getReductionCountForAnswer(clue, answer, domains, filledDomains)
            if reduction == -1:
                # One of the constraints indicates that filling this clue with specified answer will eliminate all answers for a different domain
                return -1
            total = total + reduction
        return total
    
    def reduceDomainsWithAnswer(self, clue, answer, domains):
        for constraint in self.findConstraintsForClue(clue):
            constraint.applyConstraint(clue, answer, domains)

    def removeConstraintsForClue(self, clue):
        for constraint in self.findConstraintsForClue(clue):
            self.constraints.remove(constraint)
        
    def shrinkInitialDomains(self, domains, clues):
        log('Shrinking domains according to crossword constraints. Updated Domains:', newLine=False)
        while True:
            allConstraintsAreSatisfied = True
            for constraint in self.constraints:
                acrossChars = list(map(lambda x: x[constraint.acrossIndex], domains[constraint.acrossClue]))
                downChars =  list(map(lambda x: x[constraint.downIndex], domains[constraint.downClue]))
                
                i = 0
                while i < len(domains[constraint.acrossClue]):
                    if domains[constraint.acrossClue][i][constraint.acrossIndex] not in downChars and domains[constraint.acrossClue][i] != clues[constraint.acrossClue]:
                        domains[constraint.acrossClue].remove(domains[constraint.acrossClue][i])
                        allConstraintsAreSatisfied = False
                    else:
                        i = i + 1
                    
                i = 0
                while i < len(domains[constraint.downClue]):
                    if domains[constraint.downClue][i][constraint.downIndex] not in acrossChars and domains[constraint.downClue][i] != clues[constraint.downClue]:
                        domains[constraint.downClue].remove(domains[constraint.downClue][i])
                        allConstraintsAreSatisfied = False
                    else:
                        i = i + 1
            if allConstraintsAreSatisfied:
                break