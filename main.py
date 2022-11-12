from tkinter import *
import os 
import pandas
import random
from start_page import *

BACKGROUND_COLOR ='#1e6631'

root = Tk()
root.title("Blackjack game")
root.config(padx=50, pady=50, bg = BACKGROUND_COLOR)

canvas = Canvas(width = 300, height = 300)
canvas.config(bg = BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()

startPage = startPage(root, canvas)

root.mainloop()