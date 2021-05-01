from State import State
from collections import deque, OrderedDict
import copy

def log(log):
    if type(log) == dict:
        # It is an operation
        parsedClue = log['clue'].replace('d', ' Down').replace('a', ' Across')
        if log['type'] == 'insert':
            print('Candidates for \'' + parsedClue + '\': ' + ', '.join(log['domain']))
            print('using ->', log['answer'])
        if log['type'] == 'update':
            print('undoing', log['prevAnswer'], '-> now using', log['nextAnswer'], 'for', parsedClue)
        if log['type'] == 'delete':
            print('Delete', log['answer'], 'from', parsedClue)
        else:
            print()
    else:
        print(log)

def calculateOperations(prevState, nextState):
    if prevState is None:
        return []

    prevList = list(prevState.filledDomains.items())
    nextList = list(nextState.filledDomains.items())
    if len(nextState.filledDomains) > len(prevState.filledDomains): # New answer is inserted
        return [{
            'type': 'insert', 
            'clue': nextList[len(nextState.filledDomains) - 1][0], 
            'answer': nextList[len(nextState.filledDomains) - 1][1],
            'domain': prevState.domains[nextList[len(nextState.filledDomains) - 1][0]]
        }]

    if len(nextState.filledDomains) == len(prevState.filledDomains) and len(nextState.filledDomains) != 0: # Last answer is changed
        return [{
            'type': 'update', 
            'clue': nextList[len(nextState.filledDomains) - 1][0], 
            'prevAnswer': prevList[len(nextState.filledDomains) - 1][0], 
            'nextAnswer': nextList[len(nextState.filledDomains) - 1][1]
        }]

    if len(nextState.filledDomains) < len(prevState.filledDomains): # Backtrace. Delete items from prevState one by one starting from the end
        i = len(prevState.filledDomains) - 1
        operations = []
        while i >= len(nextState.filledDomains):
            operations.append({
                'type': 'delete', 
                'clue': prevList[i][0], 
                'answer': prevList[i][1]
            })
            i = i - 1
        operations.append({
            'type': 'update', 
            'clue': nextList[i][0], 
            'prevAnswer': prevList[i][1], 
            'nextAnswer': nextList[i][1]
        })
        return operations
    
    return []

def search(initialState, handleOperation):
    # TODO: We should move this function to another place in order to show resulting puzzle with graphics

    if initialState.isGoal():
        return [initialState]
    
    currentPath = [initialState]

    queue = deque([currentPath])

    prevState = None

    while queue:
        visited = set()
        currentPath = queue.popleft()
        currentState = currentPath[len(currentPath) - 1]

        for operation in calculateOperations(prevState, currentState):
            handleOperation(operation)
            log(operation)
        
        prevState = currentState

        if currentState.isGoal():
            handleOperation({'type': 'goal'})
            log('Goal state of the puzzle is found!')
            return currentPath

        if currentState.isStuck():
            log('Puzzle is stuck! Start backtracing')
            continue

        for state in currentPath:
            visited.add(state)
        
        nextStates = currentState.getNextStates()

        for nextState in nextStates:
            if nextState in visited:
                continue
                
            tempPath = copy.deepcopy(currentPath)
            tempPath.append(nextState)
            queue.insert(0, tempPath)