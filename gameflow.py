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
        test = True
        while test is True:
            uid = getUID()
            data = getData(uid)
            test = compareHand(gameState, players, uid)
            if test is False:
                msg1 = "Invalid card"
                msg2 = "Rescan..."
                printDisplay(gameState, msg1, msg2, dummy, players)
                time.sleep(3)
                scanPlay(gameState, teams, players) 
        x = Cards() #TODO
        if gameState.leadTurn is True:
            updateRoundHand(x)
            gameState.setLead(x.suit)
            gameState.setleadTurn(False)
            msg1 = "** was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, [x.suit, x.val], disp)
            time.sleep(2)
        else:
            updateRoundHand(x)
            msg1 = "** was played"
            msg2 = "Continue..."
            printAll(msg1, msg2, [x.suit, x.val], disp)
            time.sleep(2)

def scanStart():
    uid = getUID()
    data = getData(uid)
    return suitsArray[data[3]]

#TODO either get data or create card not both
def scan(gameState, players):
    for player in players:
        uid = getUID()
        i = 0
        for card in players[gameState.turn-1].hand:
            if players[gameState.turn-1].hand[i].uid is uid:
                Confmsg1 = "Card exists"
                Confmsg2 = "Try again"
                printDisplay(gameState, msg1, msg2, dummy, players)
                time.sleep(3)
            else:
                x = Cards()
                players[gameState.turn-1].handAppend(x)
            i = i + 1

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
        time.sleep(2)
        if players[gameState.turn-1].keypad.getResponse() is 10: #N
            time.sleep(3)
            printDisplay(gameState, msg1, msg2, arr, players)
            resp = players[gameState.turn-1].keypad.getResponse()
            time.sleep(3)
        elif players[gameState.turn-1].keypad.getResponse() is 9: #Y
            time.sleep(3)
            return resp

#TODO update for player class/fix in general
def readKey(i, disp, keys):
    response = keys[i-1].getResponse()
    return response

#TODO update for player class
def compareSuit(num, gameState, teams, players):
    if gameState.roundHand[-1].suit is not gameState.lead:
        if num is 1:
            for Cards in players[0].hand:
                if players[0].hand[Cards].suit is gameState.lead:
                    gameState.renigA = True
                    msg1 = "Player 1"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
                    time.sleep(3)
        elif num is 2:
            for Cards in players[1].hand:
                if players[1].hand[Cards].suit is gameState.lead:
                    gameState.renigB = True
                    msg1 = "Player 2"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
                    time.sleep(3)
        elif num is 3:
            for Cards in players[2].hand:
                if players[2].hand[Cards].suit is gameState.lead:
                    gameState.renigA = True
                    msg1 = "Player 3"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
                    time.sleep(3)
        else:
            for Cards in players[3].hand:
                if players[3].hand[Cards].suit is gameState.lead:
                    gameState.renigB = True
                    msg1 = "Player 4"
                    msg2 = "Renig"
                    printAll(msg1, msg2, dummy, disp)
                    time.sleep(3)

#TODO update for player class/check logic
def compareHand(gameState, players, uid):
    if gameState.turn is 1:
        for Cards in players[0].hand:
            if uid is players[0].hand[Cards].uid:
                return True
        return False
    elif gameState.turn is 2:
        for Cards in players[1].hand:
            if uid is players[1].hand[Cards].uid:
                return True
        return False
    elif gameState.turn is 3:
        for Cards in players[2].hand:
            if uid is players[2].hand[Cards].uid:
                return True
        return False
    else:
        for Cards in players[3].hand:
            if uid is players[3].hand[Cards].uid:
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
        time.sleep(2)

        for k in range(5):
            scan(gameState, players)
            msg1 = "Next Card".format(gameState.turn)
            msg2 = ""
            printDisplay(gameState, msg1, msg2, dummy, players)
            time.sleep(2)

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
            time.sleep(2)
            checkHint(players, gameState)
            gameState.setRoundPlay(True)

            if j is 0:
                msg1 = "Lead with High"
                msg2 = "OffSuit"
                printDisplay(gameState, msg1, msg2, dummy, players)
                time.sleep(2)
                gameState.setleadTurn(True)

            scanPlay(gameState, teams, players)
            compareSuit(num+1, gameState, teams, players)
        scoreRound(gameState, teams, players)
        if endGame is True:
                break
        gameState.incTurn()

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
    time.sleep(2)

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
        intVal is 3
    elif val is 'Q':
        intVal is 4
    elif val is 'K':
        intVal is 5
    else:
        intVal is 6
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
                time.sleep(2)
                gameState.setRoundPlay(True)

                t = t + 1

                if t is 1:
                    gameState.setleadTurn(True)
                scanPlay(gameState, teams, players)
                compareSuit(num+1, gameState, teams, players)
        scoreRound(gameState, teams, players)
        if endGame is True:
            break
        gameState.incTurn()

#TODO confused
def compareVal(gameState):
    for Cards in gameState.roundHand:
        max = convertVal(gameState, gameState.roundHand[-1].val, gameState.roundHand[-1].suit)
        retMax = gameState.roundHand[-1].uid
        while Cards > 1:
            if convertVal(gameState, gameState.roundHand[Cards].val, gameState.roundHand[Cards].suit) > max:
                max = convertVal(gameState, gameState.roundHand[Cards].val, gameState.roundHand[Cards].suit)
                retMax = gameState.roundHand[-1].uid
    return retMax

#TODO is it needed?
def checkHand(max, teams, players):
    for Cards in players[0].hand:
        if players[0].hand[Cards].uid is max:
            return 1
    for Cards in players[1].hand:
        if players[1].hand[Cards].uid is max:
            return 2
    for Cards in players[2].hand:
        if players[2].hand[Cards].uid is max:
            return 1
    for Cards in players[3].hand:
        if players[3].hand[Cards].uid is max:
            return 2
            teams[1].updateTricks()

#TODO Double check teams and how renig score works
def awardTrick(teamTrick, teams):
    if teamTrick is 1:
        teams[0].updateTricks()
    else:
        teams[1].updateTricks()

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
    for Cards in gameState.roundHand:
        if gameState.roundHand[Cards].suit is not gameState.lead and gameState.roundHand[Cards].suit is not gameState.trump:
            del gameState.roundHand[Cards]
        elif gameState.roundHand[Cards].suit is gameState.trump:
            for Cards in gameState.roundHand:
                if gameState.roundHand[Cards].suit is not gameState.trump:
                    del gameState.roundHand[Cards]

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
                time.sleep(3)
                confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                if confResp is 9: #Y
                    msg1 = "Pick up card"
                    msg2 = "and scan"
                    printDisplay(gameState, msg1, msg2, dummy, players)
                    time.sleep(2)
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
                time.sleep(3)
                confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                if confResp is not 9 and not 10: #Y/N
                    gameState.trump = suitsArray[confResp]
                    msg1 = "Trump is *"
                    msg2 = ""
                    printAll(msg1, msg2, [gameState.trump], players)
                    time.sleep(2)
                    break
                elif confResp is not 9: #Y
                    break

        if confResp is not 10: #N
            msg1 = "Alone?(Y/n)"
            msg2 = ""
            printDisplay(gameState, msg1, msg2, dummy, players)

            resp = players[gameState.turn-1].keypad.getResponse()
            time.sleep(3)
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
                    time.sleep(3)
                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                    if confResp is 9: #Y
                        msg1 = "Pick up card"
                        msg2 = "and scan"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        time.sleep(2)
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
                    time.sleep(3)
                    confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                    if confResp is not 9 and not 10: #Y/N
                        gameState.trump = suitsArray[confResp]
                        msg1 = "Trump is *"
                        msg2 = ""
                        printAll(msg1, msg2, [gameState.trump], players)
                        time.sleep(2)
                        break
                    elif confResp is not 9: #Y
                        break

            if confResp is not 10: #N
                msg1 = "Alone?(Y/n)"
                msg2 = ""
                printDisplay(gameState, msg1, msg2, dummy, players)

                resp = players[gameState.turn-1].keypad.getResponse()
                time.sleep(3)
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
                time.sleep(3)

                if i is 0:
                    while True:
                        msg1 = "Call(Y)"
                        msg2 = "or Pass(N)"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(3)
                        confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                        if confResp is 9: #Y
                            msg1 = "Pick up card"
                            msg2 = "and scan"
                            printDisplay(gameState, msg1, msg2, dummy, players)
                            time.sleep(2)
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
                        time.sleep(3)
                        confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                        if confResp is not 9 and not 10: #Y/N
                            gameState.trump = suitsArray[confResp]
                            msg1 = "Trump is *"
                            msg2 = ""
                            printAll(msg1, msg2, [gameState.trump], players)
                            time.sleep(2)
                            break
                        elif confResp is not 9: #Y
                            break

                if confResp is not 10: #N
                    msg1 = "Alone?(Y/n)"
                    msg2 = ""
                    printDisplay(gameState, msg1, msg2, dummy, players)

                    resp = players[gameState.turn-1].keypad.getResponse()
                    time.sleep(3)
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
                            time.sleep(3)
                            confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                            if confResp is 9: #Y
                                msg1 = "Pick up card"
                                msg2 = "and scan"
                                printDisplay(gameState, msg1, msg2, dummy, players)
                                time.sleep(2)
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
                            time.sleep(3)
                            confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)
                            if confResp is not 9 and not 10: #Y/N
                                gameState.trump = suitsArray[confResp]
                                msg1 = "Trump is *"
                                msg2 = ""
                                printAll(msg1, msg2, [gameState.trump], players)
                                time.sleep(2)
                                break
                            elif confResp is not 9: #Y
                                break

                    if confResp is not 10: #N
                        msg1 = "Alone?(Y/n)"
                        msg2 = ""
                        printDisplay(gameState, msg1, msg2, dummy, players)

                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(3)
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
        time.sleep(2)
            return


def clear(gameState, players):
    gameState.clearRoundHand()
    for i in range(len(players)):
        players[i].handClear()
    self.roundPlay = False
    self.leadTurn = False
    self.turn = 1
    self.lead = suitsArray[0]
    self.trump = suitsArray[0]
    self.renigA = False
    self.renigB = False
    self.endGame = False

#main game
def main(gameState, teams, players):
    initCustChars(players)
    for j in range(1,19):
        #default player 1 deal
        dealRound(gameState, players)
        gameState.setTurn(gameState.deal)
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
            time.sleep(3)
            reset(gameState, teams, players)
            gameState.incDeal()

if __name__ == '__main__':
    gameState =  gameState()

    P1 = player(1, I2C_ADP1, 1)
    players = [P1]

    ATeam = Team()
    teams = [ATeam]
try:
    main(gameState, teams, players)
except KeyboardInterrupt:
    pass
finally:
    P1.lcd.lcd_byte(0x01, LCD_CMD)
