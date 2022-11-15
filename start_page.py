from tkinter import *
import os 
import pandas
import random
from PIL import ImageTk, Image


class startPage:

    wd = os.getcwd()
    BACKGROUND_COLOR ='#1e6631'

    dealer_score = 0
    mine_score = 0

    def __init__(self, root, canvas):

        for child in canvas.winfo_children():
            child.destroy()

        self.data = pandas.read_csv(self.wd + '/cards.csv')
        self.data = self.data.to_dict(orient="records")

        # try:
        #     self.data = pandas.read_csv(self.wd + '/Blackjack_project/new_cards.csv')
        #     self.data = self.data.to_dict(orient="records")
        # except:
        #     self.data = pandas.read_csv(self.wd + '/Blackjack_project/cards.csv')
        #     self.data = self.data.to_dict(orient="records")

        self.back_image = Image.open(self.wd + '/images/background.png')
        self.back_image = self.back_image.resize((120, 200), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(self.back_image)

        self.opponent_1 = Label(canvas, image = self.back_image, bg = self.BACKGROUND_COLOR)
        self.opponent_1.grid(row=0, column=0)
        self.opponent_2 = Label(canvas, image = self.back_image, bg = self.BACKGROUND_COLOR)
        self.opponent_2.grid(row=0, column=1)

        self.mine_1 = Label(canvas, image = self.back_image, bg = self.BACKGROUND_COLOR)
        self.mine_1.grid(row=2, column=0)
        self.mine_2 = Label(canvas, image = self.back_image, bg = self.BACKGROUND_COLOR)
        self.mine_2.grid(row=2, column=1)

        self.placeholder_card_img = Image.open(self.wd + '/images/placeholder_card.png')
        self.placeholder_card_img = ImageTk.PhotoImage(self.placeholder_card_img)

        self.placeholder_between_img = Image.open(self.wd + '/images/placeholder_between.png')
        self.placeholder_between_img = ImageTk.PhotoImage(self.placeholder_between_img)

        self.placeholder_bewteen = Label(canvas, image=self.placeholder_between_img, bg = self.BACKGROUND_COLOR)

        self.placeholder_bewteen.grid(row=1,column=0, sticky=N+S+E+W, padx=0, pady=0)
        
        self.opponent_3 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.opponent_3.grid(row=0,column=2)

        self.opponent_4 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.opponent_4.grid(row=0,column=3)

        self.opponent_5 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.opponent_5.grid(row=0,column=4)

        self.mine_3 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.mine_3.grid(row=2,column=2)

        self.mine_4 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.mine_4.grid(row=2,column=3)

        self.mine_5 = Label(canvas, image=self.placeholder_card_img, bg = self.BACKGROUND_COLOR)
        self.mine_5.grid(row=2,column=4)

        # Buttons
        right_image = PhotoImage(file= self.wd + '/images/right.png')
        button_right = Button(canvas,image=right_image, borderwidth = 0, highlightthickness=0, command=lambda: self.withdraw_card(root, canvas))
        button_right.image = right_image
        button_right.grid(row=2, column=5)

        wrong_image = PhotoImage(file= self.wd + '/images/wrong.png')
        button_wrong = Button(canvas, image=wrong_image, borderwidth = 0, highlightthickness=0, command=lambda: self.withdraw_card(root, canvas))
        button_wrong.image = wrong_image
        button_wrong.grid(row=2, column=6)

        self.starting_card(root, canvas)

    def starting_card(self, root, canvas):
        self.opp_card_1 = random.choice(self.data)
        self.data.remove(self.opp_card_1)

        self.opp_card_2 = random.choice(self.data)
        self.data.remove(self.opp_card_2)

        self.opp_card_2_image = Image.open(self.wd + f'/images/{self.opp_card_2["value"]}_of_{self.opp_card_2["suit"]}.png')
        self.opp_card_2_image = self.opp_card_2_image.resize((120, 200), Image.ANTIALIAS)
        self.opp_card_2_image = ImageTk.PhotoImage(self.opp_card_2_image)

        self.opponent_2.config(image=self.opp_card_2_image)

        self.mine_card_1 = random.choice(self.data)
        self.data.remove(self.mine_card_1)

        self.mine_card_1_image = Image.open(self.wd + f'/images/{self.mine_card_1["value"]}_of_{self.mine_card_1["suit"]}.png')
        self.mine_card_1_image = self.mine_card_1_image.resize((120, 200), Image.ANTIALIAS)
        self.mine_card_1_image = ImageTk.PhotoImage(self.mine_card_1_image)

        self.mine_1.config(image=self.mine_card_1_image)

        self.mine_card_2 = random.choice(self.data)
        self.data.remove(self.mine_card_2)

        self.mine_card_2_image = Image.open(self.wd + f'/images/{self.mine_card_2["value"]}_of_{self.mine_card_2["suit"]}.png')
        self.mine_card_2_image = self.mine_card_2_image.resize((120, 200), Image.ANTIALIAS)
        self.mine_card_2_image = ImageTk.PhotoImage(self.mine_card_2_image)

        self.mine_2.config(image=self.mine_card_2_image)

        self.score_update()

        # Buttons
        dealer_score_label = Label(canvas,text='Dealer: ?', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        dealer_score_label.grid(row=1, column=5)

        mine_score_label = Label(canvas,text=f'Chunbae: {self.mine_score}', bg = self.BACKGROUND_COLOR, font = 'Helvetica 14')
        mine_score_label.grid(row=1, column=6)


    def withdraw_card(self, root, canvas):
        pass

    def score_update(self):

        if self.opp_card_1["value"] in ('jack', 'queen', 'king'):
            self.opp_card_1["value"] = 10
        elif self.opp_card_1["value"] == 'ace':
            self.opp_card_1["value"] = [1, 10]
        else:
            self.opp_card_1["value"] = int(self.opp_card_1["value"])
        
        if self.opp_card_2["value"] in ('jack', 'queen', 'king'):
            self.opp_card_2["value"] = 10
        elif self.opp_card_2["value"] == 'ace':
            self.opp_card_2["value"] = [1, 10]
        else:
            self.opp_card_2["value"] = int(self.opp_card_2["value"])
        
        if self.mine_card_1["value"] in ('jack', 'queen', 'king'):
            self.mine_card_1["value"] = 10
        elif self.mine_card_1["value"] == 'ace':
            self.mine_card_1["value"] = [1, 10]
        else:
            self.mine_card_1["value"] = int(self.mine_card_1["value"])

        
        if self.mine_card_2["value"] in ('jack', 'queen', 'king'):
            self.mine_card_2["value"] = 10
        elif self.mine_card_2["value"] == 'ace':
            self.mine_card_2["value"] = [1, 10]
        else:
            self.mine_card_2["value"] = int(self.mine_card_2["value"])

        self.dealer_score = self.opp_card_1["value"] + self.opp_card_2["value"]
        self.mine_score = self.mine_card_1["value"] + self.mine_card_2["value"]
