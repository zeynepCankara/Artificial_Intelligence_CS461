"""
@Date: 28/02/2021 ~ Version: 1.3
@Author: Ege Şahin

@Description: Converter of arrays to user interface with the help of custom tkinter widget (Cell)

"""

from tkinter import * 
from parsePuzzle import parsePuzzle
from Cell import Cell
from datetime import datetime

def showAnswers(boxList):
    i = 0
    for cell in puzzleInformation['cells']:
        if(cell["cellNumber"] != -1):
            boxList[i].reveal()
        i += 1
        
def hideAnswers(boxList):
    i = 0
    for cell in puzzleInformation['cells']:
        if(cell["cellNumber"] != -1):
            boxList[i].hide()
        i += 1
       
puzzleInformation = parsePuzzle()

# creating main tkinter window/toplevel 
master = Tk()

# Creating Title of Across Clues
l0 = Label(master, text = "ACROSS", font = 'franklin 13 bold')
l0.grid(row = 0, column = 5, rowspan = 1, sticky = W, padx = 10)

# Creating Across Clues
i = 0
acrossClues = []
for clueNumber, clue in puzzleInformation['acrossClues'].items():
    acrossClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    acrossClues[i].grid(row = i + 1, column = 5, sticky = W, rowspan = 1, padx = 10)
    i += 1

# Creating Title of Down Clues
i += 3
l1 = Label(master, text = "DOWN", font = 'franklin 13 bold')
l1.grid(row = i, column = 5, rowspan = 1, sticky = W, padx = 10)

# Creating Down Clues
downClues = []
j = 0
for clueNumber, clue in puzzleInformation['downClues'].items():
    downClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    downClues[j].grid(row = i + 1, column = 5, sticky = W, rowspan = 1, padx = 10)
    i += 1
    j += 1

# Creating puzzle Information
k = 0
boxList = []
for cell in puzzleInformation['cells']:
    if(cell["cellNumber"] == -1):
        boxList.append(Cell(master, isBlack=True))
    else:
        if(cell["cellNumber"] != 0):
            newCell = Cell(master, number=cell["cellNumber"], letter = cell['letter'])
            newCell.hide()
            boxList.append(newCell)
        else:
            newCell = Cell(master, letter = cell['letter'])
            newCell.hide()
            boxList.append(newCell)
    boxList[k].grid(row = (int(k / 5) * 3), column = (k % 5), rowspan = 3)
    k += 1
    
# Button for showing actions
button1 = Button(master, bg="white", relief="solid", text = "Click for Anwers", command=lambda: showAnswers(boxList))
button1.grid(row = i + 3, column = 5)

button2 = Button(master, bg="white", relief="solid", text = "Hide the Anwers", command=lambda: hideAnswers(boxList))
button2.grid(row = i + 4, column = 5, pady = 10)

now = datetime.now()
dateLabel = Label(master, text = now.strftime("Group Name: RIDDLER\nDate : %d-%m-%Y\nTime : %H:%M:%S"), font="franklin 14")
dateLabel.grid(row = 16, column = 2, columnspan = 3, rowspan = 2, sticky = "e")
  
mainloop() 

