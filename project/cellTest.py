"""
@Date: 28/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç

@Description: Test for custom Tkinter widget: Cell

"""

from tkinter import *
from Cell import Cell

master = Tk()

black = Cell(master, isBlack=True)
black.grid(row=0, column=0)

withNumber = Cell(master, number=1, letter="A")
withNumber.grid(row=0, column=1)

withoutNumber = Cell(master, letter="B")
withoutNumber.grid(row=0, column=2)

falseCell = Cell(master) #Although it is handled inside Cell class, letter should be defined everytime unless it is black
falseCell.grid(row=0, column=3)

def revealAll():
    for children in master.winfo_children():
        if type(children) == Cell:
            children.reveal()

def hideAll():
    for children in master.winfo_children():
        if type(children) == Cell:
            children.hide()

show = Button(master, bg="white", relief="solid", text = "Show", command=lambda: revealAll())
show.grid(row=1, column=0)

hide = Button(master, bg="white", relief="solid", text = "Hide", command=lambda: hideAll())
hide.grid(row=1, column=2)

mainloop()