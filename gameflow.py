#!/usr/python
#main gameplay/rules
import binascii
import sys
import smbus
import time

from cardClass import Cards
from cardClass import getUID
from cardClass import getData
from LCD_Class import lcd
from LCD_Class import i2c_device
from keypad import keypad
from playerClass import player
from playerClass import Team
from playerClass import gameState

dummy = [] #dummy array
#hearts, spades, diamond, club
suitsArray = [unichr(0),unichr(0),unichr(1),unichr(2),unichr(3)]

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
def initCustChars(players):
    for i in range(len(players)):
        players[i].lcd.custom_char(heartChar, 0)
        players[i].lcd.custom_char(spadeChar, 1)
        players[i].lcd.custom_char(diamondChar, 2)
        players[i].lcd.custom_char(clubChar, 3)
        
def reset(gameState, teams, players):
    for mem in  teams:
        teams[mem].score = 0
        teams[mem].tricks = 0
        teams[mem].Called = False
        teams[mem].Alone = False
    for p in players:
        players[p].handClear()
    gameState.clearRoundHand()
    gameState.roundPlay = False
    gameState.leadTurn = False
    gameState.turn = 1
    gameState.lead = suitsArray[0]
    gameState.trump = suitsArray[0]
    gameState.renigA = False
    gameState.renigB = False
    gameState.endGame = False

#??? TODO
def scanPlay(gameState, teams, players):
        #SCANS card
        #test = True
        uid = getUID()
        data = getData(uid)
        #test = compareHand(gameState, players, uid)
        #if test is False:
            #msg1 = "Invalid card"
            #msg2 = "Rescan..."
            #printDisplay(gameState, msg1, msg2, dummy, players)
            #time.sleep(1)
            #scanPlay(gameState, teams, players) 
        x = Cards() #TODO
        if gameState.leadTurn is True:
            gameState.roundHand(x)
            gameState.setLead(x.suit)
            gameState.setleadTurn(False)
            msg1 = "** was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, [x.suit, x.val], players)
            time.sleep(1)
        else:
            gameState.roundHand(x)
            msg1 = "** was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, [x.suit, x.val], players)
            time.sleep(1)

def scanStart():
    uid = getUID()
    data = getData(uid)
    return suitsArray[data[3]]

#TODO either get data or create card not both
def scan(gameState, players):
    uid = getUID()
    for card in players[gameState.turn-1].hand:
        if players[gameState.turn-1].hand[i].uid is uid:
            msg1 = "Card exists"
            msg2 = "Try again"
            printDisplay(gameState, msg1, msg2, dummy, players)
            time.sleep(1)
            scan(gameState, players)   
    x = Cards()
    players[gameState.turn-1].handAppend(x)
      

#TODO update for player class
def printDisplay(gameState, msg1, msg2, arr, players):
    players[gameState.turn-1].lcd.lcd_byte(0x01, LCD_CMD)
    if not arr:
        players[gameState.turn-1].lcd.lcd_string(msg1, LCD_LINE_1)
        players[gameState.turn-1].lcd.lcd_string(msg2, LCD_LINE_2)
    else: 
        players[gameState-1].lcd.lcd_custom_str(msg1, arr)
        players[gameState-1].lcd.lcd_string(msg2, LCD_LINE_2)
    
#TODO update for player class
def printAll(msg1, msg2, arr, players):
    for i in range(len(players)):
        players[i].lcd.lcd_byte(0x01, LCD_CMD)
        if not arr:
            players[i].lcd.lcd_string(msg1, LCD_LINE_1)
            players[i].lcd.lcd_string(msg2, LCD_LINE_2)
        else:
            players[i].lcd.lcd_custom_str(msg1, arr, LCD_LINE_1)
            players[i].lcd.lcd_string(msg2, LCD_LINE_2)

def playerConfirm(gameState, msg1, msg2, arr, players, resp):
    while True:
        Confmsg1 = "Are you sure?"
        Confmsg2 = "Y/n"
        printDisplay(gameState, Confmsg1, Confmsg2, dummy, players)
        time.sleep(1)
        if players[gameState.turn-1].keypad.getResponse() is 10: #N
            time.sleep(1)
            printDisplay(gameState, msg1, msg2, arr, players)
            resp = players[gameState.turn-1].keypad.getResponse()
            time.sleep(1)
        elif players[gameState.turn-1].keypad.getResponse() is 9: #Y
            time.sleep(1)
            return resp

#TODO update for player class/fix in general
def readKey(i, players, keys):
    response = keys[i-1].getResponse()
    return response

#TODO update for player class
def compareSuit(num, gameState, teams, players):
    i = 0
    if gameState.roundHand[-1].suit is not gameState.lead:
        if num is 1:
            for Cards in players[0].hand:
                if players[0].hand[i].suit is gameState.lead:
                    gameState.renigA = True
                    msg1 = "Player 1"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, players)
                    time.sleep(2)
                i = i + 1
        elif num is 2:
            for Cards in players[1].hand:
                if players[1].hand[i].suit is gameState.lead:
                    gameState.renigB = True
                    msg1 = "Player 2"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, players)
                    time.sleep(2)
                i = i + 1
        elif num is 3:
            for Cards in players[2].hand:
                if players[2].hand[i].suit is gameState.lead:
                    gameState.renigA = True
                    msg1 = "Player 3"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, players)
                    time.sleep(2)
                i = i + 1
        else:
            for Cards in players[3].hand:
                if players[3].hand[i].suit is gameState.lead:
                    gameState.renigB = True
                    msg1 = "Player 4"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, players)
                    time.sleep(2)
                i = i + 1

#TODO update for player class/check logic
def compareHand(gameState, players, uid):
    i = 0
    if gameState.turn is 1:
        for i in players[0].hand:
            if uid is players[0].hand[i].uid:
                return True
        return False
    elif gameState.turn is 2:
        for i in players[1].hand:
            if uid is players[1].hand[i].uid:
                return True
        return False
    elif gameState.turn is 3:
        for i in players[2].hand:
            if uid is players[2].hand[i].uid:
                return True
        return False
    else:
        for i in players[3].hand:
            if uid is players[3].hand[i].uid:
                return True
        return False

#TODO update for player class
def scanHands(gameState, players):
    for num in range(4):
        msg1 = "Wait..."
        msg2 = ""
        printAll(msg1, msg2, dummy, players)
        time.sleep(1)
        #Players SCAN cards
        msg1 = "Player {}".format(gameState.turn)
        msg2 = "Scan Cards"
        printDisplay(gameState, msg1, msg2, dummy, players)
        time.sleep(1)

        for k in range(5):
            uid = getUID()
            data = getData(uid)
            scan(gameState, players)
            msg1 = "Player {}".format(gameState.turn)
            msg2 = "Cards Scanned {}".format(k+1)
            printDisplay(gameState, msg1, msg2, dummy, players)
            time.sleep(1)

        gameState.incTurn()

#TODO update for player class/ check flow or logic
def playRound(gameState, teams, players):
    gameState.setTurn(gameState.deal)
    gameState.incTurn()

    scanHands(gameState, players)
    for k in range(5):
        for j in range(4):
            msg1 = "Wait..."
            msg2 = ""
            printAll(msg1, msg2, dummy, players)
            time.sleep(1)

            msg1 = "Play Card"
            msg2 = "For Turn"
            printDisplay(gameState, msg1, msg2, dummy, players)
            time.sleep(1)
            checkHint(players, gameState)
            gameState.setRoundPlay(True)

            if j is 0:
                msg1 = "Lead with High"
                msg2 = "OffSuit"
                printDisplay(gameState, msg1, msg2, dummy, players)
                time.sleep(1)
                gameState.setleadTurn(True)

            scanPlay(gameState, teams, players)
            #compareSuit(gameState.turn, gameState, teams, players)
        scoreRound(gameState, teams, players)
        if gameState.endGame is True:
                break
        gameState.incTurn()
        callPass(gameState, teams, players)

def printHint(gameState, players, hint):
    if hint is 1:
        msg1 = "* Was Lead"
        msg2 = "Follow Suit"
        printDisplay(gameState, msg1, msg2, gameState.lead, players)
    elif hint is 2:
        msg1 = "Play Higher *"
        msg2 = ""
        printDisplay(gameState, msg1, msg2, gameState.trump, players)
    else:
        msg1 = "Play Low"
        msg2 = "OffSuit"
        printDisplay(gameState, msg1, msg2, dummy, players)
    time.sleep(1)

def checkHint(players, gameState):
    hint = 0
    for Cards in players[gameState.turn-1].hand:
        if players[gameState.turn-1].hand[Cards].suit is gameState.lead:
            hint = 1
            break   
        elif players[gameState.turn-1].hand[Cards].suit is gameState.trump:
            for i in gameState.roundHand:
                if gameState.roundHand[i].trump is gameState.trump:
                    if convertInt(gameState, players[gameState.turn-1].hand[Cards].val, players[gameState.turn-1].hand[Cards].suit) > convertInt(gameState, gameState.roundHand[i].val, gameState.roundHand[i].suit):
                        hint = 2           
        else:
            if hint is not 2:
                hint = 0
        printHint(gameState, players, hint)
        
def convertInt(gameState, val, suit):
    if val is '9':
        intVal = 1
    elif val is 'T':
        intVal = 2
    elif val is 'J':
        intVal = 3
    elif val is 'Q':
        intVal = 4
    elif val is 'K':
        intVal = 5
    else:
        intVal = 6
    return adjustVal(gameState, intVal, suit)

def adjustVal(gameState, intVal, suit):
    if gameState.trump is suit:
        intVal = intVal + 20
        if intVal is 23:
            intVal = intVal + 10
    elif gameState.trump is suitsArray[1]:
        gameState.opposite = suitsArray[3]
        if gameState.opposite is suit:
            if intVal is 3:
                intVal = intVal + 25
    elif gameState.trump is suitsArray[2]:
        gameState.opposite = suitsArray[4]
        if gameState.opposite is suit:
            if intVal is 3:
                intVal = intVal + 25
    elif gameState.trump is suitsArray[3]:
        gameState.opposite = suitsArray[1]
        if gameState.opposite is suit:
            if intVal is 3:
                intVal = intVal + 25
    elif gameState.trump is suitsArray[4]:
        gameState.opposite = suitsArray[2]
        if gameState.opposite is suit:
            if intVal is 3:
                intVal = intVal + 25
    elif gameState.lead is suit:
        intVal = intVal + 10
    else:
        intVal = intVal
    return intVal
    
    

#TODO update for player class/ check flow or logic
def playAlone(loner, gameState, teams, players):
    gameState.setTurn(gameState.deal)
    gameState.incTurn()
    t=0

    scanHands(gameState, players)
    for k in range(5):
        for j in range(4):
            if gameState.turn+2 is loner:
                gameState.incTurn()
            elif gameState.turn-2 is loner:
                gameState.incTurn()
            else:
                msg1 = "Wait..."
                msg2 = ""
                printAll(msg1, msg2, dummy, players)
                time.sleep(1)

                msg1 = "Play Card"
                msg2 = "For Turn"
                printDisplay(gameState, msg1, msg2, dummy, players)
                time.sleep(1)
                gameState.setRoundPlay(True)
                checkHint(players, gameState)
                time.sleep(1)

                t = t + 1

                if t is 1:
                    gameState.setleadTurn(True)
                scanPlay(gameState, teams, players)
                #compareSuit(gameState.turn, gameState, teams, players)
        scoreRound(gameState, teams, players)
        if gameState.endGame is True:
            break
        gameState.incTurn()
        callPass(gameState, teams, players)

#TODO confused
def compareVal(gameState):
    i = 0
    for Cards in gameState.roundHand:
        max = convertInt(gameState, gameState.roundHand[-1].val, gameState.roundHand[-1].suit)
        retMax = gameState.roundHand[-1].uid
        if len(gameState.roundHand) > 1:
            if convertInt(gameState, gameState.roundHand[i].val, gameState.roundHand[i].suit) > max:
                max = convertInt(gameState, gameState.roundHand[i].val, gameState.roundHand[i].suit)
                retMax = gameState.roundHand[i].uid
        i = i + 1
        
    return retMax

#TODO is it needed?
def checkHand(max, teams, players):
    i = 0
    for Cards in players[0].hand:
        if players[0].hand[i].uid is max:
            return 1
    for Cards in players[1].hand:
        if players[1].hand[i].uid is max:
            return 2
    for Cards in players[2].hand:
        if players[2].hand[i].uid is max:
            return 1
    for Cards in players[3].hand:
        if players[3].hand[i].uid is max:
            return 2

#TODO Double check teams and how renig score works
def awardTrick(teamTrick, teams):
    if teamTrick is 1:
        teams[0].updateTricks()
        msg1 = "Team A Takes"
        msg2 = "The Trick"
        printAll(msg1, msg2, dummy, players)
    else:
        teams[1].updateTricks()
        msg1 = "Team B Takes"
        msg2 = "The Trick"
        printAll(msg1, msg2, dummy, players)

#TODO move renig checks into this func
def checkScore(gameState, teams):
    if gameState.renigA is True:
        teams[1].updateScore(2)
    elif gameState.renigB is True:
        teams[0].updateScore(2)
    elif teams[0].tricks is 5:
        if teams[0].Alone is True:
            teams[0].updateScore(4)
        else:
            teams[0].updateScore(2)
    elif teams[0].tricks >= 3:
        if teams[1].Called is True:
            teams[0].updateScore(2)
        else:
            teams[0].updateScore(1)
    elif teams[1].tricks is 5:
        if teams[1].Alone is True:
            teams[1].updateScore(4)
        else:
            teams[1].updateScore(2)
    elif teams[1].tricks >= 3:
        if teams[0].Called is True:
            teams[1].updateScore(2)
        else:
            teams[1].updateScore(1)

    if teams[1].score >= 10:
         gameState.setEndGame(True)
    if teams[1].score >= 10:
        gameState.setEndGame(True)

#TODO double check deletion and logic
def scoreRound(gameState, teams, players):
    i = 0
    j = 0
    for Cards in gameState.roundHand:
        if gameState.roundHand[i].suit is not gameState.lead: 
            if gameState.roundHand[i].suit is not gameState.trump:
                del gameState.roundHand[i]
            elif gameState.roundHand[i].suit is gameState.trump:
                for Cards in gameState.roundHand:
                    if gameState.roundHand[j].suit is not gameState.trump:
                        del gameState.roundHand[j]
                    j = j + 1
        i = i + 1

    teamTrick = checkHand(compareVal(gameState), teams, players)
    awardTrick(teamTrick, teams)
    checkScore(gameState, teams)

#TODO logic and update
def callPass(gameState, teams, players):
    #Player 2, call/pass
    for i in range(2):
        gameState.incTurn()

        msg1 = "Wait..."
        msg2 = ""
        printAll(msg1, msg2, dummy, players)
        time.sleep(1)

        if i is 0:
            while True:
                msg1 = "Call(Y)"
                msg2 = "or Pass(N)"
                printDisplay(gameState, msg1, msg2, dummy, players)
                resp = players[gameState.turn-1].keypad.getResponse()
                time.sleep(0.5)
                confResp = 1
                if resp is not 9:
                    if resp is not 10:
                        confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                if confResp is 9: #Y
                    msg1 = "Pick up card"
                    msg2 = "and scan"
                    printDisplay(gameState, msg1, msg2, dummy, players)
                    time.sleep(0.5)
                    gameState.setTrump(scanStart())

                    msg1 = "Trump is *"
                    msg2 = ""
                    printAll(msg1, msg2, [gameState.trump], players)
                    time.sleep(2)
                    break
                elif confResp is 10: #N
                    break
        else:
            while True:
                msg1 = "Call(Suit)"
                msg2 = "or Pass(N)"
                printDisplay(gameState, msg1, msg2, dummy, players)
                resp = players[gameState.turn-1].keypad.getResponse()
                time.sleep(0.5)
                confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                if confResp is not 10: #N
                    if confResp is not 9: #Y
                        gameState.trump = suitsArray[confResp]
                        msg1 = "Trump is *"
                        msg2 = ""
                        printAll(msg1, msg2, [gameState.trump], players)
                        time.sleep(2)
                        break
                else: 
                    break

        if confResp is not 10: #N
            msg1 = "Alone?(Y/n)"
            msg2 = ""
            printDisplay(gameState, msg1, msg2, dummy, players)

            resp = players[gameState.turn-1].keypad.getResponse()
            time.sleep(1)
            confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)

            teams[(gameState.turn-1)%2].updateCalled(True)

            if confResp is 9: #Y
                teams[(gameState.turn-1)%2].updateAlone(True)
                playAlone(gameState.turn, gameState, teams, players)
            else:
                playRound(gameState, teams, players)

        else:
            gameState.incTurn()
            
            msg1 = "Wait..."
            msg2 = ""
            printAll(msg1, msg2, dummy, players)
            time.sleep(1)

            if i is 0:
                while True:
                    msg1 = "Call(Y)"
                    msg2 = "or Pass(N)"
                    printDisplay(gameState, msg1, msg2, dummy, players)
                    resp = players[gameState.turn-1].keypad.getResponse()
                    time.sleep(1)
                    confResp = 1
                    if resp is not 9:
                        if resp is not 10:
                            confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                    if confResp is 9: #Y
                        msg1 = "Pick up card"
                        msg2 = "and scan"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        time.sleep(1)
                        gameState.setTrump(scanStart())

                        msg1 = "Trump is *"
                        msg2 = ""
                        printAll(msg1, msg2, [gameState.trump], players)
                        time.sleep(2)
                        break
                    elif confResp is 10: #N
                        break
            else:
                while True:
                    msg1 = "Call(Suit)"
                    msg2 = "or Pass(N)"
                    printDisplay(gameState, msg1, msg2, dummy, players)
                    resp = players[gameState.turn-1].keypad.getResponse()
                    time.sleep(1)
                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                    if confResp is not 10: #N
                        if confResp is not 9: #Y
                            gameState.trump = suitsArray[confResp]
                            msg1 = "Trump is *"
                            msg2 = ""
                            printAll(msg1, msg2, [gameState.trump], players)
                            time.sleep(2)
                            break
                    else: 
                        break

            if confResp is not 10: #N
                msg1 = "Alone?(Y/n)"
                msg2 = ""
                printDisplay(gameState, msg1, msg2, dummy, players)

                resp = players[gameState.turn-1].keypad.getResponse()
                time.sleep(1)
                confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)

                teams[(gameState.turn-1)%2].updateCalled(True)

                if confResp is 9: #Y
                    teams[(gameState.turn-1)%2].updateAlone(True)
                    playAlone(gameState.turn, gameState, teams, players)
                else:
                    playRound(gameState, teams, players)
            else:
                gameState.incTurn()
            
                msg1 = "Wait..."
                msg2 = ""
                printAll(msg1, msg2, dummy, players)
                time.sleep(2)

                if i is 0:
                    while True:
                        msg1 = "Call(Y)"
                        msg2 = "or Pass(N)"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(1)
                        confResp = 1
                        if resp is not 9:
                            if resp is not 10:
                                confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                        if confResp is 9: #Y
                            msg1 = "Pick up card"
                            msg2 = "and scan"
                            printDisplay(gameState, msg1, msg2, dummy, players)
                            time.sleep(1)
                            gameState.setTrump(scanStart())

                            msg1 = "Trump is *"
                            msg2 = ""
                            printAll(msg1, msg2, [gameState.trump], players)
                            time.sleep(2)
                            break
                        elif confResp is 10: #N
                            break
                else:
                    while True:
                        msg1 = "Call(Suit)"
                        msg2 = "or Pass(N)"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(1)
                        confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                        if confResp is not 10: #N
                            if confResp is not 9: #Y
                                gameState.trump = suitsArray[confResp]
                                msg1 = "Trump is *"
                                msg2 = ""
                                printAll(msg1, msg2, [gameState.trump], players)
                                time.sleep(2)
                                break
                        else: 
                            break

                if confResp is not 10: #N
                    msg1 = "Alone?(Y/n)"
                    msg2 = ""
                    printDisplay(gameState, msg1, msg2, dummy, players)

                    resp = players[gameState.turn-1].keypad.getResponse()
                    time.sleep(1)
                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)

                    teams[(gameState.turn-1)%2].updateCalled(True)

                    if confResp is 9: #Y
                        teams[(gameState.turn-1)%2].updateAlone(True)
                        playAlone(gameState.turn, gameState, teams, players)
                    else:
                        playRound(gameState, teams, players)
                else: 
                    #Screw the dealer
                    gameState.incTurn()
            
                    msg1 = "Wait..."
                    msg2 = ""
                    printAll(msg1, msg2, dummy, players)
                    time.sleep(1)

                    if i is 0:
                        while True:
                            msg1 = "Call(Y)"
                            msg2 = "or Pass(N)"
                            printDisplay(gameState, msg1, msg2, dummy, players)
                            resp = players[gameState.turn-1].keypad.getResponse()
                            time.sleep(1)
                            confResp = 1
                            if resp is not 9:
                                if resp is not 10:
                                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                            if confResp is 9: #Y
                                msg1 = "Pick up card"
                                msg2 = "and scan"
                                printDisplay(gameState, msg1, msg2, dummy, players)
                                time.sleep(1)
                                gameState.setTrump(scanStart())

                                msg1 = "Trump is *"
                                msg2 = ""
                                printAll(msg1, msg2, [gameState.trump], players)
                                time.sleep(2)
                                break
                            elif confResp is 10: #N
                                break
                    else:
                        while True:
                            msg1 = "Call(Suit)"
                            msg2 = ""
                            printDisplay(gameState, msg1, msg2, dummy, players)
                            resp = players[gameState.turn-1].keypad.getResponse()
                            time.sleep(1)
                            confresp = 10
                            if resp is not 9:
                                if resp is not 10:
                                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                            if confResp is not 10: #N
                                if confResp is not 9: #Y
                                    gameState.trump = suitsArray[confResp]
                                    msg1 = "Trump is *"
                                    msg2 = ""
                                    printAll(msg1, msg2, [gameState.trump], players)
                                    time.sleep(2)
                                    break

                    if confResp is not 10: #N
                        msg1 = "Alone?(Y/n)"
                        msg2 = ""
                        printDisplay(gameState, msg1, msg2, dummy, players)

                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(1)
                        confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)

                        teams[(gameState.turn-1)%2].updateCalled(True)

                        if confResp is 9: #Y
                            teams[(gameState.turn-1)%2].updateAlone(True)
                            playAlone(gameState.turn, gameState, teams, players)
                        else:
                            playRound(gameState, teams, players)
         
def dealRound(gameState, players):
    i = gameState.deal
    msg1 = "Wait..."
    msg2 = ""
    printAll(msg1, msg2, dummy, players)
    time.sleep(2)
    msg1 = "Deal 5 Cards per"
    msg2 = "player    Y-cont"
    printDisplay(gameState, msg1, msg2, dummy, players)
    while True:
        if players[i-1].keypad.getResponse() is 9: #Y
            time.sleep(1)
            return


def clear(gameState, players):
    gameState.clearRoundHand()
    for i in range(len(players)):
        players[i].handClear()
    gameState.roundPlay = False
    gameState.leadTurn = False
    gameState.turn = 1
    gameState.lead = suitsArray[0]
    gameState.trump = suitsArray[0]
    gameState.renigA = False
    gameState.renigB = False
    gameState.endGame = False

#main game
def main(gameState, teams, players):
    initCustChars(players)
    for j in range(1,19):
        #default player 1 deal
        dealRound(gameState, players)
        gameState.setTurn(gameState.deal)
        #callPass vs Main loop
        callPass(gameState, teams, players) 
        clear(gameState, players) 
        if teams[0].score >= 10:
            msg1 = "TEAM A"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy, players)
            break
        elif teams[1].score >=10:
            msg1 = "TEAM B"
            msg2 = "WINNER"
            printAll(msg1, msg2, dummy, players)
            break
        else:
            msg1 = "Next Deal"
            msg2 = "Continue..."
            printAll(msg1, msg2, dummy, players)
            time.sleep(1)
            reset(gameState, teams, players)
            gameState.incDeal()

if __name__ == '__main__':
    gameState =  gameState()

    P1 = player(1, I2C_ADP1, 1)
    P2 = player(1, I2C_ADP2, 1)
    P3 = player(1, I2C_ADP3, 1)
    P4 = player(1, I2C_ADP4, 1)
    players = [P1, P2, P3, P4]

    ATeam = Team()
    BTeam = Team()
    teams = [ATeam, BTeam]
    
try:
    main(gameState, teams, players)
except KeyboardInterrupt:
    pass
finally:
    P1.lcd.lcd_byte(0x01, LCD_CMD)
    P2.lcd.lcd_byte(0x01, LCD_CMD)
    P3.lcd.lcd_byte(0x01, LCD_CMD)
    P4.lcd.lcd_byte(0x01, LCD_CMD)
