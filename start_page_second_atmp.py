from tkinter import *
import os 
import pandas
import random
from PIL import ImageTk, Image


class startPage:

    wd = os.getcwd()
    BACKGROUND_COLOR ='#1e6631'
    
    opponent_turn = 1 
    mine_turn = 1

    opponent_score = 0
    mine_score = 0

    opponent_x = 0
    opponent_y = 0

    mine_x = 0
    mine_y = 250

    def __init__(self, root, canvas):

        for child in canvas.winfo_children():
            child.destroy()

        self.data = pandas.read_csv(self.wd + '/cards.csv')
        self.data = self.data.to_dict(orient="records")

        self.back_image = Image.open(self.wd + '/images/background.png')
        self.back_image = self.back_image.resize((120, 200), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(self.back_image)

        # Buttons
        right_image = PhotoImage(file= self.wd + '/images/right.png')
        button_right = Button(canvas,image=right_image, borderwidth = 0, highlightthickness=0, command=lambda: self.withdraw_card(root, canvas))
        button_right.image = right_image
        button_right.place(x=800,y=300)

        wrong_image = PhotoImage(file= self.wd + '/images/wrong.png')
        button_wrong = Button(canvas, image=wrong_image, borderwidth = 0, highlightthickness=0, command=lambda: self.stop_card(root, canvas))
        button_wrong.image = wrong_image
        button_wrong.place(x=900,y=300)

        self.starting_card(root, canvas)

    def starting_card(self, root, canvas):
        for i in range(0, 2):
            self.opponent(root, canvas, self.opponent_turn)

        for i in range(0, 2):
            self.mine(root, canvas, self.mine_turn)
        
        # Buttons
        dealer_score_label = Label(canvas,text='Dealer: ?', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        dealer_score_label.place(x=800,y=150)

        mine_score_label = Label(canvas,text=f'Chunbae: {self.mine_score}', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        mine_score_label.place(x=900,y=150)

    def withdraw_card(self, root, canvas):
        self.mine(root, canvas, self.mine_turn)

        if self.mine_score > 21:
            self.losing_label(root, canvas)
            return

        self.opponent(root, canvas, self.opponent_turn)

        dealer_score_label = Label(canvas,text='Dealer: ?', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        dealer_score_label.place(x=800,y=150)

        mine_score_label = Label(canvas,text=f'Chunbae: {self.mine_score}', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        mine_score_label.place(x=900,y=150)

    def stop_card(self, root, canvas):
        self.opponent_1 = Image.open(self.wd + f'/images/{self.opponent_1["value"]}_of_{self.opponent_1["suit"]}.png')
        self.opponent_1 = self.opponent_1.resize((120, 200), Image.ANTIALIAS)
        self.opponent_1 = ImageTk.PhotoImage(self.opponent_1)
            
        self.opponent_1_label = Label(canvas, image = self.opponent_1, bg = self.BACKGROUND_COLOR)
        self.opponent_1_label.image = self.opponent_1
        self.opponent_1_label.place(x=0, y=0)

        dealer_score_label = Label(canvas,text=f'Dealer: {self.opponent_score}', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        dealer_score_label.place(x=800,y=150)

        if self.opponent_score > 21:
            self.winning_label(root, canvas)
            return

        elif self.opponent_score > 17 and self.opponent_score > self.mine_score:
            self.losing_label(root, canvas)
            return

        while (self.opponent_score <= 17):
            self.opponent(root, canvas, self.opponent_turn)
            
            dealer_score_label = Label(canvas,text=f'Dealer: {self.opponent_score}', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
            dealer_score_label.place(x=800,y=150)

        if self.opponent_score <= 21 and self.opponent_score > self.mine_score:
            self.losing_label(root, canvas)
            return

        elif self.opponent_score > 21:
            self.winning_label(root, canvas)
            return

    def mine(self, root, canvas, mine_turn):
        self.mine_card = random.choice(self.data)
        self.data.remove(self.mine_card)

        self.mine_image = Image.open(self.wd + f'/images/{self.mine_card["value"]}_of_{self.mine_card["suit"]}.png')
        self.mine_image = self.mine_image.resize((120, 200), Image.ANTIALIAS)
        self.mine_image = ImageTk.PhotoImage(self.mine_image)
        
        self.mine_card_label = Label(canvas, image = self.mine_image, bg = self.BACKGROUND_COLOR)
        self.mine_card_label.image = self.mine_image

        self.mine_card_label.place(x=self.mine_x, y=self.mine_y)
        self.mine_x += 130

        self.mine_score = self.score_update(self.mine_card["value"], self.mine_score)
        # print("mine_score", self.mine_score)

        self.mine_turn += 1

    def opponent(self, root, canvas, opponent_turn):
        self.opponent_card = random.choice(self.data)
        self.data.remove(self.opponent_card)

        self.opp_image = Image.open(self.wd + f'/images/{self.opponent_card["value"]}_of_{self.opponent_card["suit"]}.png')
        self.opp_image = self.opp_image.resize((120, 200), Image.ANTIALIAS)
        self.opp_image = ImageTk.PhotoImage(self.opp_image)

        if self.opponent_turn == 1:
            self.opponent_card_label = Label(canvas, image = self.back_image, bg = self.BACKGROUND_COLOR)
            self.opponent_card_label.image = self.back_image
            self.opponent_1 = self.opponent_card
        else:
            self.opponent_card_label = Label(canvas, image = self.opp_image, bg = self.BACKGROUND_COLOR)
            self.opponent_card_label.image = self.opp_image

        self.opponent_card_label.place(x=self.opponent_x, y=self.opponent_y)
        self.opponent_x += 130

        self.opponent_score = self.score_update(self.opponent_card["value"], self.opponent_score)
        # print("opponent_score", self.opponent_score)

        self.opponent_turn += 1

    def score_update(self, score, total_score):
        if score in ('jack', 'queen', 'king'):
            score = 10
        elif score == 'ace':
            score = 1
        else:
            score = int(score)

        total_score = total_score + score
        # print("total_score", total_score)
        return(total_score)

    def winning_label(self, root, canvas):
        self.winning_label = Label(canvas, text='Chunbae won!', font = ('Helvetica', 30), fg='red', bg='white', borderwidth = 1, relief='solid', padx= 5, pady=5)
        self.winning_label.place(x=390, y=190)

        self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 15), borderwidth = 1, highlightthickness=0, command = lambda:self.restart(root, canvas))
        self.restart_btn.place(x=440, y=250)

    def losing_label(self, root, canvas):
        self.winning_label = Label(canvas, text='Chunbae lost!', font = ('Helvetica', 30), fg='red', bg='white', borderwidth = 1, relief='solid', padx= 5, pady=5)
        self.winning_label.place(x=390, y=190)

        self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 15), borderwidth = 1, highlightthickness=0, command = lambda:self.restart(root, canvas))
        self.restart_btn.place(x=440, y=250)

    def restart(self, root, canvas):
        restartPage = startPage(root, canvas)
