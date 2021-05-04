def log(log, newLine=True):
    if type(log) == dict:
        # It is an operation
        parsedClue = log['clue'].replace('d', ' Down').replace('a', ' Across')
        if log['type'] == 'insert':
            print('Candidates for ' + log['longClue'] + ': ' + ', '.join(log['domain']) + ' -> using ' + log['answer'])
        if log['type'] == 'update':
            print('undoing', log['prevAnswer'], '-> now using', log['nextAnswer'], 'for', log['longClue'])
        if log['type'] == 'delete':
            print('Delete', log['answer'], 'from', log['longClue'])
    else:
        print(log)
    if newLine:
        print()

def getClueFromShortVersion(shortVersion, puzzleInformation):
    # Input: 1a -> Output: Clue string for 1 Across with specified puzzle
    if 'a' in shortVersion:
        return '\'' + puzzleInformation['acrossClues'][int(shortVersion[0])] + '\''
    else:
        return '\'' + puzzleInformation['downClues'][int(shortVersion[0])] + '\''

def getFilledCells(puzzleInformation, filledDomains):
    cells = set()
    for domain, answer in filledDomains.items():
        if answer == '':
            continue
        i = -2
        for j in range(0,25):
            if puzzleInformation['cells'][j]['cellNumber'] == int(domain[0]):
                i = j
                break
        if 'a' in domain:
            while True:
                cells.add(i)
                i = i + 1
                if i == 25 or puzzleInformation['cells'][i]['cellNumber'] == -1 or i % 5 == 0:
                    break
        else:
            while i < 25 and puzzleInformation['cells'][i]['cellNumber'] != -1:
                cells.add(i)
                i = i + 5
    return list(cells)