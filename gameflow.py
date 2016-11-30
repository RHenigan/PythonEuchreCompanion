#!/usr/python
#main gameplay/rules

from cardClass import Cards
from cardClass import getUID
from cardClass import getData
from LCD_Class import lcd
from LCD_Class import i2c_device
from keypad import keypad

global P1Hand
global P2Hand
global P3Hand
global P4Hand
global dummy
global roundHand
global playerPass
global roundPlay
global lead
global renigA
global renigB
global Ateam
global Bteam
global endGame
global tricksA
global tricksB
global scoreA
global scoreB
global i
global suitsArray
global dealer


P1Hand = []
P2Hand = []
P3Hand = []
P4Hand = []
roundHand = []
dummy = [] #dummy array
suitsArray = [unichr(0),unichr(0),unichr(1),unichr(2),unichr(3)]
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
dealer = 1

I2C_ADP1 = 0x3f # I2C device address
I2C_ADP2 = 0x3e # I2C device address
I2C_ADP3 = 0x23 # I2C device address
I2C_ADP4 = 0x25 # I2C device address
LCD_WIDTH = 16   # Max chars per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

heartChar = (
    0b00000,
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000)
diamondChar = (
    0b00000,
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000)
clubChar = (
    0b00000,
    0b01110,
    0b01110,
    0b11111,
    0b11111,
    0b00100,
    0b01110,
    0b00000)
spadeChar = (
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b01010,
    0b00100,
    0b01110,
    0b00000)

#init custom chars
def initCustChars(disp):
    for i in range(len(disp)):
        disp[i].custom_char(heartChar, 0)
        disp[i].custom_char(spadeChar, 1)
        disp[i].custom_char(diamondChar, 2)
        disp[i].custom_char(clubChar, 3)
        



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
        while test is True:
            uid = getUID()
            data = getData(uid)
            test = compareHand(i,uid)
            if test is False:
                msg1 = "Invalid card"
                msg2 = "Rescan..."
                printDisplay(i, msg1, msg2, dummy, disp)
                scanPlay() 
        x = Cards(uid, data[2], suitsArray[data[3]])
        if lead is True:
            roundHand.append(x)
            leadSuit = roundHand[-1].suit
            lead = False
            msg1 = "was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, [x.suit, x.val], disp)
        else:
            appendHand(x)

def scan():
    uid = getUID()
    data = getData(uid)
    x = Cards(uid, data[2], suitsArray[data[3]])
    appendHand(x)

def appendHand(x):
    if roundPlay is True:
        roundHand.append(x)
        roundPlay = False
        msg1 = "was played"
        msg2 = "Continue..."
        printAll(msg1, msg2, [x.suit, x.val], disp)
    elif i is 1:
        P1Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, [x.suit, x.val], disp)
    elif i is 2:
        P2Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, [x.suit, x.val], disp)
    elif i is 3:
        P3Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, [x.suit, x.val], disp)
    else: 
        P4Hand.append(x)
        msg1 = "was scanned"
        msg2 = "Continue..."
        printDisplay(i, msg1, msg2, [x.suit, x.val], disp)

def printDisplay(i, msg1, msg2, arr, disp):
    disp[i-1].lcd_byte(0x01, LCD_CMD)
    if not arr:
        disp[i-1].lcd_string(msg1, LCD_LINE_1)
        disp[i-1].lcd_string(msg2, LCD_LINE_2)
    else: 
        tempmsg = "** " + msg1
        disp[i-1].lcd_custom_str(tempmsg, arr)
        disp[i-1].lcd_string(msg2, LCD_LINE_2)
    
        
def printAll(msg1, msg2, arr, disp):
    for i in range(len(disp)):
        disp[i].lcd_byte(0x01, LCD_CMD)
        if not arr:
            disp[i].lcd_string(msg1, LCD_LINE_1)
            disp[i].lcd_string(msg2, LCD_LINE_2)
        else:
            tempmsg = "** " + msg1
            disp[i].lcd_custom_str(tempmsg, arr)
            disp[i].lcd_string(msg2, LCD_LINE_2)

def player(i):
    if i < 4:
        i+= 1
    else:
        i = 1 

def readKey(response):
    if response is 'S':
        msg1 = "SPADES is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy, disp)
    elif response is 'H':
        msg1 = "HEARTS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy, disp)
    elif response is 'D':
        msg1 = "DIAMONDS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy, disp)
    elif response is 'C':
        msg1 = "CLUBS is"
        msg2 = "Trump"
        printAll(msg1, msg2, dummy, disp)
    elif response is 'P':
        playerPass = True
        msg1 = "Player {}".format(i) 
        msg2 = "Pass"
        printAll(msg1, msg2, dummy, disp)

def compareSuit():
    if roundHand[-1].suit is not leadSuit:
        if i is 1:
            for Cards in P1Hand:
                if P1Hand[Cards].suit is leadSuit:
                    renigA = True
                    msg1 = "Player 1"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
        elif i is 2:
            for Cards in P2Hand:
                if P2Hand[Cards].suit is leadSuit:
                    renigB = True
                    msg1 = "Player 2"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
        elif i is 3:
            for Cards in P3Hand:
                if P3Hand[Cards].suit is leadSuit:
                    renigA = True
                    msg1 = "Player 3"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
        else:
            for Cards in P4Hand:
                if P4Hand[Cards].suit is leadSuit:
                    renigB = True
                    msg1 = "Player 4"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)

def compareHand():
    if i is 1:
        for Cards in P1Hand:
            if uid is P1Hand[Cards].uid:
                return True
            else:
                return False
    elif i is 2:
        for Cards in P2Hand:
            if uid is P2Hand[Cards].uid:
                return True
            else:
                return False
    elif i is 3:
        for Cards in P3Hand:
            if uid is P3Hand[Cards].uid:
                return True
            else:
                return False
    else:
        for Cards in P4Hand:
            if uid is P4Hand[Cards].uid:
                return True
            else:
                return False

def scanHands():
    for num in range(1,4):
        #Players SCAN cards
        msg1 = "Player {}".format(i)
        msg2 = "Scan Cards"
        printDisplay(i, msg1, msg2, dummy, disp)
        for k in range(5):
            scan()
        player(i)

def playRound():
    if i is 2 or i is 4:
        ATeam = True
    else:
        BTeam = True
    scanHands()
    player(dealer)
    for k in range(1,5):
        msg1 = "Player {}".format(i)
        msg2 = "Turn"
        printAll(msg1, msg2, dummy, disp)
        roundPlay = True
        lead = True
        scanPlay()
        for num in range(1,3):    
            player(i)
            roundPlay = True
            scanPlay()
            compareSuit()
        scoreRound()
        if endGame is True:
            break
        player(i)

def playAlone():
    scanHands()
    player(dealer)
    if i is alone + 1:
        player(i)
    for k in range(1,5):
        if i is alone + 1:
            player(i)
        else: 
            msg1 = "Player {}".format(i)
            msg2 = "Turn"
            printAll(msg1, msg2, dummy, disp)
            roundPlay = True
            lead = True
            scanPlay()
            for num in range(1,3):    
                player(i)
                roundPlay = True
                scanPlay()
                compareSuit()
            scoreRound()
            if endGame is True:
                break
            player(i)

def compareVal():
    for Cards in roundHand:
        max = roundHand[-1].uid
        while Cards > 1:
            if roundHand[Cards].val > max:
                max = roundHand[Cards].uid
    return max

def checkHand(max):
    for Cards in P1Hand:
        if P1Hand[Cards].uid is max:
            i = 1
    for Cards in P2Hand:
        if P2Hand[Cards].uid is max:
            i = 2
    for Cards in P3Hand:
        if P3Hand[Cards].uid is max:
            i = 3
    for Cards in P4Hand:
        if P4Hand[Cards].uid is max:
            i = 4

def awardTrick():
    if i is 1 or i is 3:
        if renigA is False:
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
        if ATeam is True:
            scoreA = scoreA + 1
        else:
            scoreA = scoreA + 2
    elif tricksB >= 3:
        if BTeam is True:
            scoreB = scoreB + 1
        else:
            scoreB = scoreB + 2
    if scoreA >= 10:
         endGame = True
    if scoreB >= 10:
        endGame = True

def scoreRound():
    for Cards in roundHand:
        if roundHand[Cards].suit is not leadSuit and roundHand[Cards].suit is not trump:
            del roundHand[Cards]
        elif roundHand[Cards].suit is trump:
            for Cards in roundHand:
                if roundHand[Cards].suit is not trump:
                    del roundHand[Cards]

    checkHand(compareVal())
    awardTrick()
    checkScore()

def callPass(disp):
    #Player 2, call/pass
    player(dealer)
    msg1 = "Player {}".format(i)
    msg2 = "Call or Pass"
    printDisplay(i, msg1, msg2, dummy, disp)
    readKey(getResponse())
    if playerPass == False:
        teamB = True
        readKey(getResponse())
        if getResponse() == 'A':
            playAlone()
        else:
            playRound()
    else:
        player(i) #Player 3
        msg1 = "Player {}".format(i)
        msg2 = "Call or Pass"
        printDisplay(i, msg1, msg2, dummy, disp)
        readKey(getResponse())
        if playerPass == False:
            teamA = True
            readKey(getResponse())
            if getResponse() == 'A':
                playAlone()
            else:
                playRound()
        else:
            player(i) #Player 4
            msg1 = "Player {}".format(i)
            msg2 = "Call or Pass"
            printDisplay(i, msg1, msg2, dummy, disp)
            readKey(getResponse())
            if playerPass == False:
                teamB = True
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
                printDisplay(i, msg1, msg2, dummy, disp)
                readKey(response)
                #alone
                readKey(getResponse())
                teamA = True
                if getResponse() == 'A':
                    playAlone()
                else:
                    playRound()

def dealRound(disp):
    dealer = i
    msg1 = "Wait..."
    msg2 = ""
    printAll(msg1, msg2, dummy, disp)
    msg1 = "Player {}".format(i)
    msg2 = "Deal"
    printDisplay(i, msg1, msg2, dummy, disp)

def clear():
    for Cards in RoundHand:
        del RoundHand[Cards]
    for Cards in P1Hand:
        del P1Hand[Cards]
    for Cards in P2Hand:
        del P2Hand[Cards]
    for Cards in P3Hand:
        del P3Hand[Cards]
    for Cards in P4Hand:
        del P4Hand[Cards]

#main game
def main(P1Disp):
    disp = [P1Disp]
    initCustChars(disp)
    for j in range(1,19):
        #default player 1 deal
        dealRound(disp)
        callPass(disp) 
        clear() 
        if scoreA >= 10:
            msg1 = "TEAM A"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy, disp)
            break
        elif scoreB >=10:
            msg1 = "TEAM B"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy, disp)
            break
        else:
            msg1 = "Next Deal"
            msg2 = "Continue..."
            printAll(msg1, msg2, dummy, disp)
            reset()
            player(dealer)

if __name__ == '__main__':
    P1Disp = lcd(I2C_ADP1, 1)
    #P2Disp = lcd(I2C_ADP2, 1)
    #P3Disp = lcd(I2C_ADP3, 1)
    #P4Disp = lcd(I2C_ADP4, 1)

try:
    main(P1Disp)
except KeyboardInterrupt:
    pass
finally:
    P1Disp.lcd_byte(0x01, LCD_CMD)
    #P2Disp.lcd_byte(0x01, LCD_CMD)
    #P3Disp.lcd_byte(0x01, LCD_CMD)
    #P4Disp.lcd_byte(0x01, LCD_CMD)