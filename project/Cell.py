"""
@Date: 28/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Custom Tkinter widget for rendering cells of crossword puzzle

"""

from tkinter import * 

class Cell(Frame):
    def __init__(self, parent, isBlack=False, number=None, letter=None):
        Frame.__init__(self, parent, height=100, width=100, bg="black" if isBlack else "white", highlightthickness=1)
        self.config(highlightbackground='grey')
        self.isBlack = isBlack
        if not isBlack:
            
            if number:
                self.topLeft = topleft = Label(self, text=number, font="franklin 20", bg="white")
                topleft.place(relx=0.05, rely=0.05, anchor=NW)

            if letter:
                self.letter = Label(self, text=letter, font="franklin 45 bold",bg="white")
    
    def hide(self):
        if hasattr(self, "letter"):
            self.letter.place_forget()
        self.changeColor('tomato')
        
    def reveal(self):
        if hasattr(self, "letter"):
            self.letter.place(relx=0.5, rely=0.6, anchor=CENTER)
    
    def insert(self, letter):
        self.changeColor('khaki')
        self.letter.config(text=letter)
        self.reveal()
    
    def changeColor(self, color):
        if hasattr(self, 'topLeft'):
            self.topLeft.config(bg=color)
        if not self.isBlack:
            self.config(bg=color)
        if hasattr(self, 'letter'):
            self.letter.config(bg=color)