"""
@Date: 28/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç

@Description: Custom Tkinter widget for rendering cells of crossword puzzle

"""

from tkinter import * 

class Cell(Frame):
    def __init__(self, parent, isBlack=False, number=None, letter=None):
        Frame.__init__(self, parent, height=100, width=100, bg="black" if isBlack else "white", borderwidth=1, relief="solid")

        if not isBlack:
            
            if number:
                topleft = Label(self, text=number, font="franklin 20", bg="white")
                topleft.place(relx=0.05, rely=0.05, anchor=NW)

            if letter:
                self.letter = Label(self, text=letter, font="franklin 45 bold",bg="white")
    
    def hide(self):
        if hasattr(self, "letter"):
            self.letter.place_forget()

    def reveal(self):
        if hasattr(self, "letter"):
            self.letter.place(relx=0.5, rely=0.6, anchor=CENTER)