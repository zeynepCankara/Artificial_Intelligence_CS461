from State import State
from collections import deque, OrderedDict
import copy

def log(log):
    # For now, I am just printing log to the console
    # TODO: We should implement functions so that these logs (Like inserting an answer to a clue) can be seen graphically
    if type(log) == dict:
        # It is an operation
        parsedDomain = log['domain'].replace('d', ' Down').replace('a', ' Across')
        if log['type'] == 'insert':
            print('Insert', log['answer'], 'into', parsedDomain)
        if log['type'] == 'update':
            print('Change', parsedDomain, 'from', log['prevAnswer'], 'to', log['nextAnswer'])
        if log['type'] == 'delete':
            print('Delete', log['answer'], 'from', parsedDomain)
    else:
        # It is just an informative string
        print(log)

def calculateOperations(prevState, nextState):
    prevList = list(prevState.items())
    nextList = list(nextState.items())
    if len(nextState) > len(prevState): # New answer is inserted
        return [{'type': 'insert', 'domain': nextList[len(nextState) - 1][0], 'answer': nextList[len(nextState) - 1][1]}]

    if len(nextState) == len(prevState) and len(nextState) != 0: # Last answer is changed
        return [{'type': 'update', 'domain': nextList[len(nextState) - 1][0], 'prevAnswer': prevList[len(nextState) - 1][0], 'nextAnswer': nextList[len(nextState) - 1][1]}]

    if len(nextState) < len(prevState): # Backtrace. Delete items from prevState one by one starting from the end
        i = len(prevState) - 1
        operations = []
        while i >= len(nextState):
            operations.append({'type': 'delete', 'domain': prevList[i][0], 'answer': prevList[i][1]})
            i = i - 1
        operations.append({'type': 'update', 'domain': nextList[i][0], 'prevAnswer': prevList[i][1], 'nextAnswer': nextList[i][1]})
        return operations
    
    return []

def search(handleOperation):
    # TODO: We should move this function to another place in order to show resulting puzzle with graphics

    initialState = State()

    if initialState.isGoal():
        return [initialState]
    
    currentPath = [initialState]

    queue = deque([currentPath])

    prevFilledDomains = OrderedDict()

    while queue:
        visited = set()
        currentPath = queue.popleft()
        currentState = currentPath[len(currentPath) - 1]

        for operation in calculateOperations(prevFilledDomains, currentState.filledDomains):
            handleOperation(operation)
            log(operation)
        
        prevFilledDomains = currentState.filledDomains

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