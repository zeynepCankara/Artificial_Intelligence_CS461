from tkinter import * 
from parsePuzzle import parsePuzzle

puzzleInformation = parsePuzzle()

# creating main tkinter window/toplevel 
master = Tk()

# Creating Title of Across Clues
l0 = Label(master, text = "ACROSS", font = 'franklin 12 bold')
l0.grid(row = 0, column = 5, rowspan = 1, sticky = W)

# Creating Across Clues
i = 0
acrossClues = []
for clueNumber, clue in puzzleInformation['acrossClues'].items():
    acrossClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 10'))
    acrossClues[i].grid(row = i + 1, column = 5, sticky = W, rowspan = 1)
    i += 1

# Creating Title of Down Clues
i += 3
l1 = Label(master, text = "DOWN", font = 'franklin 12 bold')
l1.grid(row = i, column = 5, rowspan = 1, sticky = W)

# Creating Down Clues
downClues = []
j = 0
for clueNumber, clue in puzzleInformation['downClues'].items():
    downClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 10'))
    downClues[j].grid(row = i + 1, column = 5, sticky = W, rowspan = 1)
    i += 1
    j += 1

# Creating puzzle Information
i = 0
boxList = []
for cell in puzzleInformation['cells']:
    if(cell["cellNumber"] == -1):
        boxList.append(Label(master, bg="black", borderwidth=2, relief="ridge", height=5, width=10))
    else:
        if(cell["cellNumber"] != 0):
            boxList.append(Label(master, bg="white", borderwidth=2, relief="solid", height=5, width=10, text = cell['cellNumber'], anchor = "nw"))
        else:
            boxList.append(Label(master, bg="white", borderwidth=2, relief="solid", height=5, width=10))
    boxList[i].grid(row = (int(i / 5) * 3), column = (i % 5), rowspan = 3)
    print(int(i / 5) * 4)
    i += 1    
  
mainloop() 


#If you want a border, the option is borderwidth. You can also choose the relief of the border: "flat", "raised", "sunken", "ridge", "solid", and "groove".
