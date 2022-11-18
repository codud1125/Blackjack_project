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
    opponent_y = 50

    mine_x = 0
    mine_y = 300

    def __init__(self, root, canvas, chunbae_money, money_bet):

        for child in canvas.winfo_children():
            child.destroy()

        self.chunbae_money = chunbae_money - money_bet
        self.money_bet = 100

        if self.chunbae_money < 0:
            self.gameover_label = Label(canvas, text='You are broke!', font = ('Helvetica', 40, "bold"), fg='red', bg=self.BACKGROUND_COLOR, borderwidth = 0, relief='solid', padx= 5, pady=5)
            self.gameover_label.place(x=340, y=230)

            self.restart_btn = Button(canvas, text='Want a do over...?', font = ('Helvetica', 10), borderwidth = 0, bg=self.BACKGROUND_COLOR, highlightthickness=0, command = lambda:self.restart(root, canvas, 1000, 100))
            self.restart_btn.place(x=400, y=300)

            return

        self.data = pandas.read_csv(self.wd + '/cards.csv')
        self.data = self.data.to_dict(orient="records")

        self.back_image = Image.open(self.wd + '/images/background.png')
        self.back_image = self.back_image.resize((120, 200), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(self.back_image)

        # wrong_right Buttons

        self.state = "normal" if (self.money_bet > 0) or (self.money_bet <= self.chunbae_money) else "disabled"

        self.increase_image = Image.open(self.wd + '/images/increase.png')
        self.increase_image = self.increase_image.resize((75, 75), Image.ANTIALIAS)
        self.increase_image = ImageTk.PhotoImage(self.increase_image)
        self.button_increase = Button(canvas,image=self.increase_image, state=self.state, borderwidth = 0, highlightthickness=0, command=lambda: self.increase_bet(root, canvas))
        self.button_increase.place(x=600,y=0)

        self.decrease_image = Image.open(self.wd + '/images/decrease.png')
        self.decrease_image = self.decrease_image.resize((75, 75), Image.ANTIALIAS)
        self.decrease_image = ImageTk.PhotoImage(self.decrease_image)
        self.button_decrease = Button(canvas,image=self.decrease_image, state=self.state, borderwidth = 0, highlightthickness=0, command=lambda: self.decrease_bet(root, canvas))
        self.button_decrease.place(x=830,y=0)

        self.chunbae_bet_label = Label(canvas,text=f'Bet: {self.money_bet}', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25))
        self.chunbae_bet_label.place(x=680,y=15)

        self.bet_image = Image.open(self.wd + '/images/bet.png')
        self.bet_image = self.bet_image.resize((75, 75), Image.ANTIALIAS)
        self.bet_image = ImageTk.PhotoImage(self.bet_image)
        self.button_bet = Button(canvas,image=self.bet_image, state=self.state, borderwidth = 0, highlightthickness=0, command=lambda: self.start(root, canvas))
        self.button_bet.place(x=930,y=0)

        self.chunbae_money_label = Label(canvas,text=f'Chunbae\'s money: {self.chunbae_money}', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25))
        self.chunbae_money_label.place(x=650,y=550)

    def start(self, root, canvas):
        self.button_increase.configure(state = 'disabled')
        self.button_decrease.configure(state = 'disabled')
        self.button_bet.configure(state = 'disabled')

        self.starting_card(root, canvas)

    def starting_card(self, root, canvas):
        # wrong_right Buttons
        right_image = PhotoImage(file= self.wd + '/images/right.png')
        self.button_right = Button(canvas,image=right_image, borderwidth = 0, highlightthickness=0, command=lambda: self.withdraw_card(root, canvas))
        self.button_right.image = right_image
        self.button_right.place(x=700,y=350)

        wrong_image = PhotoImage(file= self.wd + '/images/wrong.png')
        self.button_wrong = Button(canvas, image=wrong_image, borderwidth = 0, highlightthickness=0, command=lambda: self.stop_card(root, canvas))
        self.button_wrong.image = wrong_image
        self.button_wrong.place(x=800,y=350)

        double_image = PhotoImage(file= self.wd + '/images/double_down.png')
        self.button_double = Button(canvas, image=double_image, borderwidth = 0, highlightthickness=0, command=lambda: self.double_down(root, canvas))
        self.button_double.image = double_image
        self.button_double.place(x=900,y=350)

        self.dealer_score_label = Label(canvas,text='Dealer: ?', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25, "bold"))
        self.dealer_score_label.place(x=350,y=0)

        self.mine_score_label = Label(canvas,text=f'Chunbae: {self.mine_score}', bg = self.BACKGROUND_COLOR, font = ('Helvetica', 25, "bold"))
        self.mine_score_label.place(x=350,y=550)

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
        self.button_double.configure(state='disabled')
        self.button_increase.configure(state='disabled')
        self.button_decrease.configure(state='disabled')

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
        self.button_double.configure(state='disabled')
        self.button_increase.configure(state='disabled')
        self.button_decrease.configure(state='disabled')

        self.dealer_score_label.configure(text=f'Dealer: {self.opponent_score}')

        if isinstance(self.opponent_score, list):
            if len(self.opponent_score) > 1:
                self.opponent_score_compare = max(self.opponent_score)

        self.opponent_1 = Image.open(self.wd + f'/images/{self.opponent_1["value"]}_of_{self.opponent_1["suit"]}.png')
        self.opponent_1 = self.opponent_1.resize((120, 200), Image.ANTIALIAS)
        self.opponent_1 = ImageTk.PhotoImage(self.opponent_1)
            
        self.opponent_1_label = Label(canvas, image = self.opponent_1, bg = self.BACKGROUND_COLOR)
        self.opponent_1_label.image = self.opponent_1
        self.opponent_1_label.place(x=0, y=50)

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
            self.button_right.configure(state='disabled')
            self.button_wrong.configure(state='disabled')

            self.chunbae_money = self.chunbae_money + self.money_bet

            self.winning_label = Label(canvas, text='Tie!', font = ('Helvetica', 40, "bold"), fg='red', bg=self.BACKGROUND_COLOR, borderwidth = 0, relief='solid', padx= 5, pady=5)
            self.winning_label.place(x=340, y=230)

            self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 20), borderwidth = 0, bg=self.BACKGROUND_COLOR, highlightthickness=0, command = lambda:self.restart(root, canvas, self.chunbae_money, 100))
            self.restart_btn.place(x=400, y=300)
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

    def double_down(self, root, canvas):
        self.money_bet = self.money_bet * 2
        self.withdraw_card(root, canvas)
        self.stop_card(root, canvas)

    def winning_label(self, root, canvas):
        self.button_right.configure(state='disabled')
        self.button_wrong.configure(state='disabled')

        self.chunbae_money = self.chunbae_money + 2*self.money_bet

        self.winning_label = Label(canvas, text='Chunbae won!', font = ('Helvetica', 40, "bold"), bg = self.BACKGROUND_COLOR, fg='red', borderwidth = 0, relief='solid', padx= 5, pady=5)
        self.winning_label.place(x=340, y=230)

        self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 20), bg = self.BACKGROUND_COLOR, borderwidth =0, highlightthickness=0, command = lambda:self.restart(root, canvas, self.chunbae_money, 100))
        self.restart_btn.place(x=400, y=300)


    def losing_label(self, root, canvas):
        self.button_right.configure(state='disabled')
        self.button_wrong.configure(state='disabled')
        
        self.chunbae_money = self.chunbae_money

        self.winning_label = Label(canvas, text='Chunbae lost!', font = ('Helvetica', 40,"bold"), bg = self.BACKGROUND_COLOR, fg='red', borderwidth = 0, relief='solid', padx= 5, pady=5)
        self.winning_label.place(x=340, y=230)

        self.restart_btn = Button(canvas, text='Restart the game', font = ('Helvetica', 20), bg = self.BACKGROUND_COLOR, borderwidth = 0, highlightthickness=0, command = lambda:self.restart(root, canvas, self.chunbae_money, 100))
        self.restart_btn.place(x=400, y=300)

    def increase_bet(self, root, canvas):
        self.money_bet += 50
        self.chunbae_money = self.chunbae_money-50

        if self.money_bet <= 0:
            self.state = 'disabled'
        else:
            self.state = 'normal'

        self.button_decrease.configure(state = self.state)

        if self.chunbae_money <= 0:
            self.state = 'disabled'
        else:
            self.state = 'normal'

        self.button_increase.configure(state = self.state)

        self.chunbae_bet_label.configure(text=f'Bet: {self.money_bet}')
        self.chunbae_money_label.configure(text=f'Chunbae\'s money: {self.chunbae_money}')

    def decrease_bet(self, root, canvas):
        self.money_bet -= 50
        self.chunbae_money = self.chunbae_money+50

        if self.money_bet <= 0:
            self.state = 'disabled'
        else:
            self.state = 'normal'

        self.button_decrease.configure(state = self.state)

        if self.chunbae_money <= 0:
            self.state = 'disabled'
        else:
            self.state = 'normal'

        self.button_increase.configure(state = self.state)

        self.chunbae_bet_label.configure(text=f'Bet: {self.money_bet}')
        self.chunbae_money_label.configure(text=f'Chunbae\'s money: {self.chunbae_money}')

    def restart(self, root, canvas, chunbae_money, money_bet):
        restartPage = startPage(root, canvas, chunbae_money, money_bet)
