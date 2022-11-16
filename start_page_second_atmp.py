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
        button_right.place(x=760,y=180)

        wrong_image = PhotoImage(file= self.wd + '/images/wrong.png')
        button_wrong = Button(canvas, image=wrong_image, borderwidth = 0, highlightthickness=0, command=lambda: self.stop_card(root, canvas))
        button_wrong.image = wrong_image
        button_wrong.place(x=860,y=180)

        self.starting_card(root, canvas)

    def starting_card(self, root, canvas):

        self.dealer_score_label = Label(canvas,text='Dealer: ?', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25))
        self.dealer_score_label.place(x=720,y=80)

        self.mine_score_label = Label(canvas,text=f'Chunbae: {self.mine_score}', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25))
        self.mine_score_label.place(x=720,y=340)

        for i in range(0, 2):
            self.opponent(root, canvas, self.opponent_turn, "no")

        for i in range(0, 2):
            self.mine(root, canvas, self.mine_turn)

        if isinstance(self.mine_score, list):
            if len(self.mine_score) > 1:
                self.mine_score_compare = max(self.mine_score)
                if self.mine_score_compare == 21:
                    self.winning_label(root, canvas)
                return

    def withdraw_card(self, root, canvas):
        self.mine(root, canvas, self.mine_turn)

        if isinstance(self.mine_score, list):
            if len(self.mine_score) > 1:
                self.mine_score_compare = max(self.mine_score)
                if self.mine_score_compare > 21:
                    self.losing_label(root, canvas)
                    return
        elif self.mine_score > 21:
            self.losing_label(root, canvas)

    def stop_card(self, root, canvas):

        self.dealer_score_label.configure(text=f'Dealer: {self.opponent_score}')

        if isinstance(self.opponent_score, list):
            if len(self.opponent_score) > 1:
                self.opponent_score_compare = max(self.opponent_score)

        self.opponent_1 = Image.open(self.wd + f'/images/{self.opponent_1["value"]}_of_{self.opponent_1["suit"]}.png')
        self.opponent_1 = self.opponent_1.resize((120, 200), Image.ANTIALIAS)
        self.opponent_1 = ImageTk.PhotoImage(self.opponent_1)
            
        self.opponent_1_label = Label(canvas, image = self.opponent_1, bg = self.BACKGROUND_COLOR)
        self.opponent_1_label.image = self.opponent_1
        self.opponent_1_label.place(x=0, y=0)

        if self.opponent_score_compare > 21:
            self.winning_label(root, canvas)
            return
        elif self.opponent_score_compare > 17 and self.opponent_score_compare > self.mine_score:
            self.losing_label(root, canvas)
            return
        elif self.opponent_score_compare == 21:
            self.losing_label(root, canvas)
            return

        while (self.opponent_score_compare < 17):
            self.opponent(root, canvas, self.opponent_turn, "yes")
            if isinstance(self.opponent_score, list):
                if len(self.opponent_score) > 1:
                    self.opponent_score_compare = max(self.opponent_score)

        if isinstance(self.opponent_score, list):
            if len(self.opponent_score) > 1:
                self.opponent_score = max(self.opponent_score)

        if isinstance(self.mine_score, list):
            if len(self.mine_score) > 1:
                self.mine_score = max(self.mine_score)

        if self.opponent_score <= 21 and self.opponent_score > self.mine_score:
            self.losing_label(root, canvas)
            return
        elif self.opponent_score > 21:
            self.winning_label(root, canvas)
            return
        elif self.opponent_score < self.mine_score:
            self.winning_label(root, canvas)
            return
        elif self.opponent_score == self.mine_score:
            self.winning_label = Label(canvas, text='Tie!', font = ('Helvetica', 30), fg='red', bg='white', borderwidth = 1, relief='solid', padx= 5, pady=5)
            self.winning_label.place(x=460, y=190)

            self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 15), borderwidth = 1, highlightthickness=0, command = lambda:self.restart(root, canvas))
            self.restart_btn.place(x=440, y=250)
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

        self.score_update(self.mine_card["value"], self.mine_score, "mine", "yes")

        self.mine_turn += 1

    def opponent(self, root, canvas, opponent_turn, yes_or_no):
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

        self.score_update(self.opponent_card["value"], self.opponent_score, "opponent", yes_or_no)

        self.opponent_turn += 1

    def score_update(self, score, total_score, who, yes_or_no):
        if score in ('jack', 'queen', 'king'):
            score = 10
            if isinstance(total_score, list):
                if len(total_score) > 1:
                    self.total_score_list = [x+score for x in total_score]
                    final_score_list = []
                    for entry in self.total_score_list:
                        if entry <= 21:
                            final_score_list.append(entry)
                    total_score = final_score_list
                if len(total_score) == 1:
                    total_score = total_score[0]
            else:
                total_score = total_score + score
        elif score == 'ace':
            if isinstance(total_score, list):
                for score in total_score:
                    self.total_score_list.append(score+1)
                    self.total_score_list.append(score+11)
            else: self.total_score_list = [total_score+1, total_score+11]
            final_score_list = []
            for entry in self.total_score_list:
                if entry <= 21:
                    final_score_list.append(entry)
            total_score = final_score_list
            if isinstance(total_score, list):
                if len(total_score) == 1:
                    total_score = total_score[0]
        else:
            score = int(score)
            if isinstance(total_score, list):
                if len(total_score) > 1:
                    self.total_score_list = [x+score for x in total_score]
                    final_score_list = []
                    for entry in self.total_score_list:
                        if entry <= 21:
                            final_score_list.append(entry)
                    total_score = final_score_list
                if len(total_score) == 1:
                    total_score = total_score[0]
            else:
                total_score = total_score + score

        if who == 'opponent' and yes_or_no=='yes':
            self.opponent_score = total_score
            self.opponent_score_compare = self.opponent_score
            self.dealer_score_label.configure(text=f'Dealer: {self.opponent_score}')
        elif who == 'opponent' and yes_or_no=='no':
            self.opponent_score = total_score
            self.opponent_score_compare = self.opponent_score
            self.dealer_score_label.configure(text=f'Dealer: ?')
        elif who == 'mine':
            self.mine_score = total_score
            self.mine_score_label.configure(text=f'Chunbae: {self.mine_score}')

        return()

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
