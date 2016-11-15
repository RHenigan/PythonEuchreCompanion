#!/usr/python
#main gameplay/rules

from cardClass import Cards
from cardClass import getUID
from cardClass import getData
from LCD_Class import lcd
from LCD_Class import i2c_device
from keypad import keypad
from score import score_round
from score import score_game
from score import score_tricks


def declarations():
    temp = []
    P1Hand = []
    P2Hand = []
    P3Hand = []
    P4Hand = []
    Kitty = []
    roundHand = []
    scanKitty = False
    playerPass = False
    round = False
    i = 1

def scan():
        #SCANS card
        uid = getUID()
        data = getData(uid)
        x = Cards(uid, data[2], suitsArray[data[3]])
        temp.append(x)

def appendHand():
    z = temp[0]
    temp.remove(x)
    if scanKitty = True:
        Kitty.append(z)
        scanKitty = False
    else if round = True:
        roundHand.append(z)
        round = False
    else if i = 1:
        P1Hand.append(z)
    else if i = 2:
        P2Hand.append(z)
    else if i = 3:
        P3Hand.append(z)
    else: 
        P4Hand.append(z)

def printDisplay(i, message):
    if i = 1:
        P1Disp.lcd_string(message, LCD_LINE_1)
    else if i = 2:
        P2Disp.lcd_string(message, LCD_LINE_1)
    else if i = 3:
        P3Disp.lcd_string(message, LCD_LINE_1)
    else
        P4Disp.lcd_string(message, LCD_LINE_1)

def printAll(string)
    P1Disp.lcd_string(string, LCD_LINE_1)
    P2Disp.lcd_string(string, LCD_LINE_1)
    P3Disp.lcd_string(string, LCD_LINE_1)
    P4Disp.lcd_string(string, LCD_LINE_1)

def player(i):
    if i < 4:
        i+= 1
    else:
        i = 1 

def callTrump(response):
    if response = 'S':
        printAll("SPADES IS TRUMP")
        trump = S
    else if response = 'H':
        printAll("HEARTS IS TRUMP")
        trump = H
    else if response = 'D':
        printAll("DIAMONDS IS TRUMP")
        trump = D
    else if response = 'C':
        printAll("CLUBS IS TRUMP")
        trump = C
    else if response = 'P':
        playerPass = True
    else:

        
def renig():
#check suit against lead suit
#compare lead suit with the rest of the cards in hand
#if lead suit exists, tell player to scan proper card

def compare():
#compares suit and value of two cards

def playRound():

        for num in range(1,4)
        player(i)
        message = '"PLAYER " i " TURN"'
        printDisplay(i, message)
        print("PLAYER " i " TURN")
        #Player 2 lead - SCAN
        round = True
        scan()
        appendHand()
        if num = 1:
            #Assign lead
            
        #SCORE ROUND
        score_tricks()
        score_round()

        player(i) #reassign before the next loop/round

def playAlone():
    for num in range(1,4)
        player(i)
        if i = alone + 2:
        else:
            message = '"PLAYER " i " TURN"'
            printDisplay(i, message)
            print("PLAYER " i " TURN")
            #Player 2 lead - SCAN
            round = True
            scan()
            appendHand()
            if num = 1:
                #Assign lead
                
            #SCORE ROUND
            score_tricks()
            score_round()

            player(i) #reassign before the next loop/round

def callPass(i)
    #Player 2, call/pass
    player(i)
    message = '"PLAYER" i "CALL OR PASS"'
    printDisplay(i, message)
    print("PLAYER" i "CALL OR PASS")
    response = getResponse()
    callTrump(response)
    if playerPass = False:
        #ADD GO ALONE OPTION W/ SUB
        #alone = i
        playRound()
    else:
        player(i) #Player 3
        message = '"PLAYER" i "CALL OR PASS"'
        printDisplay(i, message)
        print("PLAYER" i "CALL OR PASS")
        response = getResponse()
        callTrump(response)
        if playerPass = False:
            playRound()
        else:
            player(i) #Player 4
            message = '"PLAYER" i "CALL OR PASS"'
            printDisplay(i, message)
            print("PLAYER" i "CALL OR PASS")
            response = getResponse()
            callTrump(response)
            if playerPass = False:
                playRound()
            else: #Screw the dealer
                player(i)
                message = '"DEALER CALL TRUMP"'
                printDisplay(i, message)
                print("DEALER CALL TRUMP")

def dealRound():
    #default Player 1 leads deal
    dealer = i
    message = '"PLAYER " i " SCAN TOP OF KITTY"'
    printDisplay(i, message)
    print("PLAYER " i " SCAN TOP OF KITTY")
    #Dealer SCAN the card
    scanKitty = True
    scan()
    appendHand()

#main game
def main():
    #begin loop
    #default player 1 deal
    message = "PLAYER " i " DEAL"
    printDisplay(i, message)
    print("PLAYER " i " DEAL")

    for num in range(1,4)
            #Players SCAN cards
            message = "PLAYER " i " SCAN CARDS"
            printDisplay(i, message)
            print("PLAYER " i " SCAN CARDS")
            for k in range(5)
                scan()
                appendHand()
                message = '"Card {0} Recorded".format(k + 1)''
                printDisplay(i, message)
                print("Card {0} Recorded".format(k + 1))
                #print("P1 Card {0}: {1} of {2}".format(i+1, P1Hand[i].val, P1Hand[i].suit))
                #raw_input("Enter for next card")
            for j in range(5):
                message = '"P" j " Card {0}: {1} of {2}".format(j+1, P1Hand[j].val, P1Hand[j].suit)''
                printDisplay(i, message)
                print("P" j " Card {0}: {1} of {2}".format(j+1, P1Hand[j].val, P1Hand[j].suit))

            cardsList[:] = []
            player(i)

  dealRound()
  callPass()

#check score to determine end of game 
score_game() 
#loop