#!/usr/bin/python

#variable declarations
score_A = 0 #int score A team
score_B = 0 #int score B team
call_A = False #bool team A call trump
call_B = False #bool team B call trump
tricks_A = 0 #number of tricks A
tricks_B = 0 #number of tricks B

#identify who takes the trick
def score_tricks(trump, lead, tricks_A, tricks_B)


#check how many points the winning team should receive
def score_round(score_A, score_B, tricks_A, tricks_B)
    if tricks_A >= 3:
        if call_A = True:
            score_A = score_A + 1 #Team A called trump, won round
        else:
            score_A = score_A + 2 #Team A Euchred Team B
    else if tricks_A >=3:
        if call_B = True:
            score_B = score_B + 1 #Team B called trump, won round
        else:
            score_B = score_B + 2 #Team B euchred Team A

#notify who the winner is
def score_game (score_A, score_B)
    if score_A > score_B:
        print("Team A WINS!!!")
    else:
        print("Team B WINS!!!")


    
    

