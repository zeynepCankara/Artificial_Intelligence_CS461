class Constraint(object):
    def __init__(self, acrossClue, acrosIndex, downClue, downIndex):
        self.acrossClue = acrossClue
        self.acrossIndex = acrosIndex
        self.downClue = downClue
        self.downIndex = downIndex
    
    def getReductionCountForAnswer(self, clue, answer, domains):
        count = 0
        if clue == self.acrossClue:
            downChars =  list(map(lambda x: x[self.downIndex], domains[self.downClue]))
            for char in downChars:
                if answer[self.acrossIndex] != char:
                    count = count + 1
        else:
            acrossChars = list(map(lambda x: x[self.acrossIndex], domains[self.acrossClue]))
            for char in acrossChars:
                if answer[self.downIndex] != char:
                    count = count + 1
        
        return count
        

class Constraints(object):
    def __init__(self, puzzleInformation):
        self.constraints = self.generateConstraints(puzzleInformation)
    
    def generateConstraints(self, puzzleInformation):
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
    
    def getTotalReductionForAnswer(self, clue, answer, domains):
        total = 0
        for constraint in self.constraints:
            if clue == constraint.acrossClue or clue == constraint.downClue:
                total = total + constraint.getReductionCountForAnswer(clue, answer, domains)
        return total
    
    def shrinkInitialDomains(self, domains):
        for constraint in self.constraints:
            acrossChars = list(map(lambda x: x[constraint.acrossIndex], domains[constraint.acrossClue]))
            downChars =  list(map(lambda x: x[constraint.downIndex], domains[constraint.downClue]))
            
            i = 0
            while i < len(domains[constraint.acrossClue]):
                if domains[constraint.acrossClue][i][constraint.acrossIndex] not in downChars:
                    domains[constraint.acrossClue].remove(domains[constraint.acrossClue][i])
                else:
                    i = i + 1
                
            i = 0
            while i < len(domains[constraint.downClue]):
                if domains[constraint.downClue][i][constraint.downIndex] not in acrossChars:
                    domains[constraint.downClue].remove(domains[constraint.downClue][i])
                else:
                    i = i + 1