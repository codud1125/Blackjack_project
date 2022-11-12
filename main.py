from tkinter import *
import os 

root = Tk()
root.title("Tic Tac Toe game")
root.config(padx=50, pady=50)

canvas = Canvas(width = 300, height = 300)
canvas.pack()

wd = os.getcwd()
print(wd)

with open(wd + '/Blackjack_project/cards.csv', 'r') as csv_line:
    card_data = csv_line.readlines()

print(card_data)