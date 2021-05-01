"""
@Date: 28/02/2021 ~ Version: 1.3
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Converter of information got from webpage to user interface with the help of custom tkinter widget (Cell)
                This converter uses grid layout which serves as a two dimesional array.

"""

from tkinter import * 
from parsePuzzle import parsePuzzle
from Cell import Cell
from datetime import datetime
from search import search
from puzzleID import puzzleID
from State import State
import time

delay = 0.5 # Seconds

initialState = State()
puzzleInformation = State.puzzleInformation

# creating main tkinter window/toplevel 
master = Tk()

# Creating Title of Across Clues and adding it to grid
l0 = Label(master, text = "ACROSS", font = 'franklin 13 bold')
l0.grid(row = 0, column = 5, rowspan = 1, sticky = W, padx = 10)

# Creating Across Clues and adding them to grid
i = 0
acrossClues = []
for clueNumber, clue in puzzleInformation['acrossClues'].items():
    acrossClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    acrossClues[i].grid(row = i + 1, column = 5, sticky = W, rowspan = 1, padx = 10, columnspan = 2)
    i += 1

# Creating Title of Down Clues and adding it to grid
i += 3
l1 = Label(master, text = "DOWN", font = 'franklin 13 bold')
l1.grid(row = i, column = 5, rowspan = 1, sticky = W, padx = 10)

# Creating Down Clues and adding them to grid
downClues = []
j = 0
for clueNumber, clue in puzzleInformation['downClues'].items():
    downClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    downClues[j].grid(row = i + 1, column = 5, sticky = W, rowspan = 1, padx = 10, columnspan = 2)
    i += 1
    j += 1

# Creating each cell of the puzzle with information from parsePuzzle and adding them to grid
k = 0
answers = []
for cell in puzzleInformation['cells']:
    if(cell["cellNumber"] == -1):
        answers.append(Cell(master, isBlack=True))
    else:
        if(cell["cellNumber"] != 0):
            newCell = Cell(master, number=cell["cellNumber"], letter = cell['letter'])
            answers.append(newCell)
        else:
            newCell = Cell(master, letter = cell['letter'])
            answers.append(newCell)
    answers[k].grid(row = (int(k / 5) * 3), column = (k % 5), rowspan = 3)
    answers[k].reveal()
    k += 1


# Creating each cell of the puzzle with information from parsePuzzle and adding them to grid
k = 0
solved = []
for cell in puzzleInformation['cells']:
    if(cell["cellNumber"] == -1):
        solved.append(Cell(master, isBlack=True))
    else:
        if(cell["cellNumber"] != 0):
            newCell = Cell(master, number=cell["cellNumber"], letter = cell['letter'])
            solved.append(newCell)
        else:
            newCell = Cell(master, letter = cell['letter'])
            solved.append(newCell)
    solved[k].grid(row = (int(k / 5) * 3), column = (k % 5 + 7), rowspan = 3)
    k += 1

# Group name label
groupLabel = Label(master, text = ("Group Name: RIDDLER"), font="franklin 14")
groupLabel.grid(row = 16, column = 9, columnspan = 3, sticky = "e")

# date label
now = datetime.now()
dateLabel = Label(master, text = now.strftime("Date : %d-%m-%Y"), font="franklin 14")
dateLabel.grid(row = 17, column = 9, columnspan = 3, sticky = "e")

# time label
timeLabel = Label(master, text = now.strftime("Time : %H:%M:%S"), font="franklin 14")
timeLabel.grid(row = 18, column = 9, columnspan = 3, sticky = "e")


def executeOperation(operation, cell, index):
    if operation['type'] == 'insert':
        cell.insert(operation['answer'][index])
        cell.changeColor('khaki')
    elif operation['type'] == 'update':
        cell.insert(operation['nextAnswer'][index])
        cell.changeColor('cyan2')
    else:
        cell.hide()

def handleOperation(operation):
    for cell in solved:
        cell.changeColor('white')

    if operation['type'] == 'goal':
        for cell in solved:
            cell.changeColor('pale green')
        return
    
    clueNumber = int(operation['clue'][0])
    if 'd' in operation['clue']:
        for i in range(0, len(puzzleInformation['cells'])):
            if puzzleInformation['cells'][i]['cellNumber'] == clueNumber:
                index = 0
                while i < 25 and puzzleInformation['cells'][i]['cellNumber'] != -1:
                    executeOperation(operation, solved[i], index)
                    i = i + 5
                    index = index + 1
                break
    elif 'a' in operation['clue']:
        for i in range(0, len(puzzleInformation['cells'])):
            if puzzleInformation['cells'][i]['cellNumber'] == clueNumber:
                index = 0
                while True:
                    executeOperation(operation, solved[i], index)
                    index = index + 1
                    i = i + 1
                    if i == 25 or puzzleInformation['cells'][i]['cellNumber'] == -1 or i % 5 == 0:
                        break
                break
    master.update()

def handleWithDelay(operation):
    time.sleep(delay)
    handleOperation(operation)

master.after(1000, search, initialState, handleWithDelay)

mainloop() 

