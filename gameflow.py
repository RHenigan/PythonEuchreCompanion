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
Global dummy
Global roundHand
Global playerPass
Global roundPlay
Global lead
Global renigA
Global renigB
Global Ateam
Global Bteam
Global endGame
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
    dummy = [] #dummy array
    playerPass = False
    roundPlay = False
    lead = False
    ATeam = False
    BTeam = False
    renigA = False
    renigB = False
    endGame = False
    tricksA = 0
    tricksB = 0
    scoreA = 0
    scoreB = 0
    i = 1

def reset():
    playerPass = False
    roundPlay = False
    lead = False
    ATeam = False
    BTeam = False  
    lead = False
    renigA = False
    renigB = False

def scanPlay():
        #SCANS card
        test = True
        While test = True
            uid = getUID()
            data = getData(uid)
            test = compareHand(i,uid)
            if test = False:
                msg1 = "Invalid card"
                msg2 = "Rescan..."
                printDisplay(i, msg1, msg2, dummy)
                scanPlay() 
        x = Cards(uid, data[2], suitsArray[data[3]])
        if lead = True:
            roundHand.append(x)
            leadSuit = roundHand[-1].suit
            lead = False
            msg1 = "was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, roundHand)
        else:
            appendHand(x)

def scan():
    uid = getUID()
    data = getData(uid)
    x = Cards(uid, data[2], suitsArray[data[3]])
    appendHand(x)

def appendHand(x):
    if roundPlay = True:
        roundHand.append(x)
        roundPlay = False
        msg1 = "was played"
        msg2 = "Continue..."
        printAll(msg1, msg2, roundHand)
    else if i = 1:
        P1Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, P1Hand)
    else if i = 2:
        P2Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, P2Hand)
    else if i = 3:
        P3Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, P3Hand)
    else: 
        P4Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, P4Hand)

def printDisplay(i, msg1, msg2, arr):
    if i = 1:
        P1Disp.lcd_byte(0x01, LCD_CMD)
        if not arr:
            P1Disp.lcd_string(msg1, LCD_LINE_1)
            P1Disp.lcd_string(msg2, LCD_LINE_2)
        else: 
            P1Disp.lcd_custom_str("** " msg1, [P1Hand[-1].val, P1Hand[-1].suit])
            P1Disp.lcd_string(msg2, LCD_LINE_2)
    else if i = 2:
        P2Disp.lcd_byte(0x01, LCD_CMD)
        if not arr:
            P2Disp.lcd_string(msg1, LCD_LINE_1)
            P2Disp.lcd_string(msg2, LCD_LINE_2)
        else:
            P2Disp.lcd_custom_str("** " msg1, [P1Hand[-1].val, P1Hand[-1].suit])
            P2Disp.lcd_string(msg2, LCD_LINE_2)
    else if i = 3:
        P3Disp.lcd_byte(0x01, LCD_CMD)
        if not arr:
            P3Disp.lcd_string(msg1, LCD_LINE_1)
            P3Disp.lcd_string(msg2, LCD_LINE_2)
        else:
            P3Disp.lcd_custom_str("** " msg1, [P1Hand[-1].val, P1Hand[-1].suit])
            P3Disp.lcd_string(msg2, LCD_LINE_2)
    else:
        P4Disp.lcd_byte(0x01, LCD_CMD)
        if not arr:
            P4Disp.lcd_string(msg1, LCD_LINE_1)
            P4Disp.lcd_string(msg2, LCD_LINE_2)
        else:
            P4Disp.lcd_custom_str("** " msg1, [P1Hand[-1].val, P1Hand[-1].suit])
            P4Disp.lcd_string(msg2, LCD_LINE_2)
        
def printAll(msg1, msg2, arr)
    P1Disp.lcd_byte(0x01, LCD_CMD)
    P2Disp.lcd_byte(0x01, LCD_CMD)
    P3Disp.lcd_byte(0x01, LCD_CMD)
    P4Disp.lcd_byte(0x01, LCD_CMD)
    if not arr:
        P1Disp.lcd_string(msg1, LCD_LINE_1)
        P1Disp.lcd_string(msg2, LCD_LINE_2)
        P2Disp.lcd_string(msg1, LCD_LINE_1)
        P2Disp.lcd_string(msg2, LCD_LINE_2)
        P3Disp.lcd_string(msg1, LCD_LINE_1)
        P3Disp.lcd_string(msg2, LCD_LINE_2)
        P4Disp.lcd_string(msg1, LCD_LINE_1)
        P4Disp.lcd_string(msg2, LCD_LINE_2)
    else:
        P1Disp.lcd_custom_str("** " msg1, [arr[-1].val, arr[-1].suit])
        P1Disp.lcd_string(msg2, LCD_LINE_2)
        P2Disp.lcd_custom_str("** " msg1, [arr[-1].val, arr[-1].suit])
        P2Disp.lcd_string(msg2, LCD_LINE_2)
        P3Disp.lcd_custom_str("** " msg1, [arr[-1].val, arr[-1].suit])
        P3Disp.lcd_string(msg2, LCD_LINE_2)
        P4Disp.lcd_custom_str("** " msg1, [arr[-1].val, arr[-1].suit])
        P4Disp.lcd_string(msg2, LCD_LINE_2)

def player(i):
    if i < 4:
        i+= 1
    else:
        i = 1 

def readKey(response):
    if response = 'S':
        msg1 = "SPADES is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy)
    else if response = 'H':
        msg1 = "HEARTS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy)
    else if response = 'D':
        msg1 = "DIAMONDS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy)
    else if response = 'C':
        msg1 = "CLUBS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy)
    else if response = 'P':
        playerPass = True
        msg1 = "Player" i 
        msg2 = "Pass"
        printAll(msg1, msg2, dummy)
    else:
        #nothing

def compareSuit():
    if roundHand[-1].suit != leadSuit:
        if i = 1:
            for Cards in P1Hand:
                if P1Hand[Cards].suit = leadSuit:
                    renigA = True
                    msg1 = "Player 1"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy)
        else if i = 2:
            for Cards in P2Hand:
                if P2Hand[Cards].suit = leadSuit:
                    renigB = True
                    msg1 = "Player 2"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy)
        else if i = 3:
            for Cards in P3Hand:
                if P3Hand[Cards].suit = leadSuit:
                    renigA = True
                    msg1 = "Player 3"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy)
        else:
            for Cards in P4Hand:
                if P4Hand[Cards].suit = leadSuit:
                    renigB = True
                    msg1 = "Player 4"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy)

def compareHand():
    if i == 1:
        for Cards in P1Hand:
            if uid == P1Hand[Cards].uid:
                return True
            else:
                return False
    else if i == 2:
        for Cards in P2Hand:
            if uid == P2Hand[Cards].uid:
                return True
            else:
                return False
    else if i == 3:
        for Cards in P3Hand:
            if uid == P3Hand[Cards].uid:
                return True
            else:
                return False
    else:
        for Cards in P4Hand:
            if uid == P4Hand[Cards].uid:
                return True
            else:
                return False

def scanHands():
    for num in range(1,4):
        #Players SCAN cards
        msg1 = "Player " i
        msg2 = "Scan Cards"
        printDisplay(i, msg1, msg2, dummy)
        for k in range(5):
            scan()
        player(i)

def playRound():
    if i == 2 or i == 4:
        ATeam = True
    else:
        BTeam = True
    scanHands()
    player(dealer)
    for k in range(1,5):
        msg1 = "Player " i
        msg2 = "Turn"
        printAll(msg1, msg2, dummy)
        roundPlay = True
        lead = True
        scanPlay()
        for num in range(1,3):    
            player(i)
            roundPlay = True
            scanPlay()
            compareSuit()
        scoreRound()
        if endGame == True:
            break
        player(i)

def playAlone():
    scanHands()
    player(dealer)
    if i == alone + 1:
        player(i)
    for k in range(1,5):
        if i == alone + 1:
            player(i)
        else: 
            msg1 = "Player " i
            msg2 = "Turn"
            printAll(msg1, msg2, dummy)
            roundPlay = True
            lead = True
            scanPlay()
            for num in range(1,3):    
                player(i)
                roundPlay = True
                scanPlay()
                compareSuit()
            scoreRound()
            if endGame == True
                break
            player(i)

def compareVal():
    for Cards in roundHand:
        max = roundHand[-1].uid
        while Cards > 1
            if roundHand[Cards].val > max:
                max = roundHand[Cards].uid
    return max

def checkHand(max):
    for Cards in P1Hand:
        if P1Hand[Cards].uid == max:
            i = 1
    for Cards in P2Hand:
        if P2Hand[Cards].uid == max:
            i = 2
    for Cards in P3Hand:
        if P3Hand[Cards].uid == max:
            i = 3
    for Cards in P4Hand:
        if P4Hand[Cards].uid == max:
            i = 4

def awardTrick():
    if i == 1 or i == 3:
        if renigA == False:
            tricksA = tricksA + 1
        else:
            renigA = False
            tricksB = tricksB + 1
    else:
        if renigB == False:
            tricksB = tricksB + 1
        else:
            renigB = False
            tricksA = tricksA + 1

def checkScore():
    if tricksA >= 3:
        if ATeam == True:
            scoreA = scoreA + 1
        else:
            scoreA = scoreA + 2
    else if tricksB >= 3:
        if BTeam == True:
            scoreB = scoreB + 1
        else:
            scoreB = scoreB + 2
    else:
        #nothing
    if scoreA >= 10 or scoreB >= 10:
        endGame = True

def scoreRound():
    for Cards in roundHand:
        if roundHand[Cards].suit != leadSuit and roundHand[Cards].suit != trump:
            del roundHand(Cards)
        else if roundHand[Cards].suit == trump:
            for Cards in roundHand:
                if roundHand[Cards].suit != trump:
                    del roundHand(Cards)
        else:
            #nothing
    checkHand(compareVal())
    awardTrick()
    checkScore()

def callPass(i):
    #Player 2, call/pass
    player(dealer)
    msg1 = "Player" i
    msg2 = "Call or Pass"
    printDisplay(i, msg1, msg2, dummy)
    readKey(getResponse())
    if playerPass == False:
        readKey(getResponse())
        if getResponse() == 'A':
            playAlone()
        else:
            playRound()
    else:
        player(i) #Player 3
        msg1 = "Player" i
        msg2 = "Call or Pass"
        printDisplay(i, msg1, msg2, dummy)
        readKey(getResponse())
        if playerPass == False:
            readKey(getResponse())
            if getResponse() == 'A':
                playAlone()
            else:
                playRound()
        else:
            player(i) #Player 4
            msg1 = "Player" i
            msg2 = "Call or Pass"
            printDisplay(i, msg1, msg2, dummy)
            readKey(getResponse())
            if playerPass == False:
                readKey(getResponse())
                if getResponse() == 'A':
                    playAlone()
                else:
                    playRound()
            else: 
                #Screw the dealer
                player(i)
                msg1 = "Dealer"
                msg2 = "Call Trump"
                printDisplay(i, msg1, msg2, dummy)
                readKey(response)
                #alone
                readKey(getResponse())
                if getResponse() == 'A':
                    playAlone()
                else:
                    playRound()

def dealRound():
    dealer = i
    msg1 = "Wait..."
    msg2 = ""
    printAll(msg1, msg2, dummy)
    msg1 = "PLAYER " i
    msg2 = "DEAL"
    printDisplay(i, msg1, msg2, dummy)

def clear():
    for Cards in RoundHand:
        del RoundHand(Cards)
    for Cards in P1Hand:
        del P1Hand(Cards)
    for Cards in P2Hand:
        del P2Hand(Cards)
    for Cards in P3Hand:
        del P3Hand(Cards)
    for Cards in P4Hand:
        del P4Hand(Cards)

#main game
def main():
    define()
    for j in range(1,19):
        #default player 1 deal
        dealRound()
        callPass() 
        clear() 
        if scoreA >=10:
            msg1 = "TEAM A"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy)
            break
        else if scoreB >=10:
            msg1 = "TEAM B"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy)
            break
        else:
            msg1 = "Next Deal"
            msg2 = "Continue..."
            printAll(msg1, msg2, dummy)
            reset()
            player(dealer)