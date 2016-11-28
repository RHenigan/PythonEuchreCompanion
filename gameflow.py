#!/usr/python
#main gameplay/rules

from cardClass import Cards
from cardClass import getUID
from cardClass import getData
from LCD_Class import lcd
from LCD_Class import i2c_device
from keypad import keypad

Global P1Hand
Global P2Hand
Global P3Hand
Global P4Hand
Global roundHand
Global playerPass
Global round
Global lead
Global Ateam
Global Bteam
Global tricksA
Global tricksB
Global scoreA
Global scoreB
Global i

def define():
    P1Hand = []
    P2Hand = []
    P3Hand = []
    P4Hand = []
    roundHand = []
    playerPass = False
    round = False
    lead = False
    ATeam = False
    BTeam = False
    tricksA = 0
    tricksB = 0
    scoreA = 0
    scoreB = 0
    i = 1

def reset():
    playerPass = False
    round = False
    lead = False
    ATeam = False
    BTeam = False  
    lead = False

def scanPlay():
        #SCANS card
        test = True
        While test = True
            uid = getUID()
            data = getData(uid)
            test = compareHand(i,uid)
            if test = False:
                #PRINT ERROR, SCAN
            else:
                #PRINT CARD 
        x = Cards(uid, data[2], suitsArray[data[3]])
        if lead = True:
            RoundHand.append(x)
            leadSuit = RoundHand[-1].suit
            lead = False
        else:
            appendHand(x)

def scan():
    uid = getUID()
    data = getData(uid)
    x = Cards(uid, data[2], suitsArray[data[3]])
    appendHand(x)

def appendHand(x):
    if round = True:
        roundHand.append(x)
        round = False
    else if i = 1:
        P1Hand.append(x)
    else if i = 2:
        P2Hand.append(x)
    else if i = 3:
        P3Hand.append(x)
    else: 
        P4Hand.append(x)

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
    else if response = 'H':
        printAll("HEARTS IS TRUMP")
    else if response = 'D':
        printAll("DIAMONDS IS TRUMP")
    else if response = 'C':
        printAll("CLUBS IS TRUMP")
    else if response = 'P':
        playerPass = True
    else:

def compareSuit():
    if RoundHand[-1].suit = leadSuit:
        #PRINTALL CARD
    else:
        #PRINT ERROR, SCAN

def compareHand():
    if i = 1:
        for Cards in P1Hand:
            if uid = P1Hand[Cards].uid
                return True
            else:
                return False
    else if i = 2:
        for Cards in P2Hand:
            if uid = P2Hand[Cards].uid
                return True
            else:
                return False
    else if i = 3:
        for Cards in P3Hand:
            if uid = P3Hand[Cards].uid
                return True
            else:
                return False
    else:
        for Cards in P4Hand:
            if uid = P4Hand[Cards].uid
                return True
            else:
                return False

def scanHands():
    for num in range(1,4)
        #Players SCAN cards
        message = "PLAYER " i " SCAN CARDS"
        printDisplay(i, message)
        print("PLAYER " i " SCAN CARDS")
        for k in range(5)
            scan()
        player(i)

def playRound():
    if i = 2 or i = 4:
        ATeam = True
    else:
        BTeam = True
    scanHands()
    player(dealer)
    for k in range(1,5)
        message = '"PLAYER " i " TURN"'
        printDisplay(i, message)
        print("PLAYER " i " TURN")
        round = True
        lead = True
        scanPlay()
        for num in range(1,3):    
            player(i)
            round = True
            scanPlay()
            compareSuit()
        scoreRound()
        scoreGame()
        if gameScore >=10:
            break
        player(i)

def playAlone():
    scanHands()
    player(dealer)
    if i = dealer + 1:
    else: 
        for k in range(1,5)
            if i = dealer + 1:
            else: 
                message = '"PLAYER " i " TURN"'
                printDisplay(i, message)
                print("PLAYER " i " TURN")
                round = True
                lead = True
                scanPlay()
                for num in range(1,3):    
                    player(i)
                    round = True
                    scanPlay()
                    compareSuit()
                scoreGame()
                if gameScore >=10:
                    break
                player(i)

def compareVal()
    for Cards in RoundHand:
        while Cards > 1
            if RoundHand[Cards].val > RoundHand[Cards+1].val:
                max = RoundHand[Cards].uid
            else
                max = RoundHand[Cards+1].uid
    return max

def checkHand(max)
    for Cards in P1Hand
        if P1Hand[Cards].uid = max:
            i = 1
    for Cards in P2Hand
        if P2Hand[Cards].uid = max:
            i = 2
    for Cards in P3Hand
        if P3Hand[Cards].uid = max:
            i = 3
    for Cards in P4Hand
        if P4Hand[Cards].uid = max:
            i = 4

def awardTrick():
    if i = 1 or i = 3
        tricksA = tricksA + 1
    else:
        tricksB = tricksB + 1

def checkScore():
    if tricksA >= 3:
        if ATeam = True:
            scoreA = scoreA + 1
        else:
            scoreA = scoreA + 2
    else if tricksB >= 3:
        if BTeam = True:
            scoreB = scoreB + 1
        else:
            scoreB = scoreB + 2
    else:
        #nothing

def scoreRound():
    for Cards in RoundHand:
        if RoundHand[Cards].suit != leadSuit and RoundHand[Cards].suit != trump:
            RoundHand[Cards].remove
        else if RoundHand[Cards].suit = trump:
            for Cards in RoundHand:
                if RoundHand[Cards].suit != trump:
                    RoundHand[Cards].remove
        else:
            #nothing
        checkHand(compareVal())
        awardTrick()
        checkScore()

def callPass(i):
    #Player 2, call/pass
    player(dealer)
    message = '"PLAYER" i "CALL OR PASS"'
    printDisplay(i, message)
    print("PLAYER" i "CALL OR PASS")
    trump = getResponse()
    callTrump(trump)
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
            else: 
                #Screw the dealer
                player(i)
                message = '"DEALER CALL TRUMP"'
                printDisplay(i, message)
                print("DEALER CALL TRUMP")
                response = getResponse()
                callTrump(response)
                playRound()

def dealRound():
    dealer = i
    message = "PLAYER " i " DEAL"
    printDisplay(i, message)
    print("PLAYER " i " DEAL")

def clear()
    for Cards in RoundHand:
        RoundHand[Cards].remove
    for Cards in P1Hand:
        P1Hand[Cards].remove
    for Cards in P2Hand:
        P2Hand[Cards].remove
    for Cards in P3Hand:
        P3Hand[Cards].remove
    for Cards in P4Hand:
        P4Hand[Cards].remove

#main game
def main():
    define()
    for j in range(1,19)
        #default player 1 deal
        dealRound()
        callPass() 
        clear() 
        if scoreA >=10:
            #PRINTALL A WINS
            break
        else if scoreB >=10:
            #PRINTALL B WINS
            break
        else:
            #PRINTALL NEXT DEAL
            reset()