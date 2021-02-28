"""
@Date: 25/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç

@Description: Test for New York Times Mini Crossword Parser

"""

from parsePuzzle import parsePuzzle

puzzleInformation = parsePuzzle()

print('Across clues:')
for clueNumber, clue in puzzleInformation['acrossClues'].items():
    print(clueNumber, clue)

print('\nDown clues:')
for clueNumber, clue in puzzleInformation['downClues'].items():
    print(clueNumber, clue)

print('\nCell Numbers(-1 if black, 0 if empty):')
i = 0
for cell in puzzleInformation['cells']:
    if i == 5:
        print()
        i = 0
    print("%2d" % cell['cellNumber'], end=' ')
    i = i + 1

print('\nSolution:')
i = 0
for cell in puzzleInformation['cells']:
    if i == 5:
        print()
        i = 0
    print(cell['letter'], end=' ')
    i = i + 1