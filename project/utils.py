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