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
I2C_ADP3 = 0x3b # I2C device address
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

def playerConfirm(gameState, msg1, msg2, arr, players, resp):
    while True:
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

def dealRound(gameState, teams, players):
	printAll("Wait...", "", [], players)
	time.sleep(2)
	msg1 = "Deal 5 Cards per".format(gameState.turn)
	msg2 = "player    Y-Cont"
	printDisplay(gameState, msg1, msg2, [], players)
	while True:
            if players[gameState.deal-1].keypad.getResponse() is 9: #Y
                time.sleep(2)
                return

def scanHands(gameState, teams, players):
	for num in range(len(players)):
		printAll("Wait...", "", [], players)
		time.sleep(1)
		msg1 = "Player {}".format(gameState.turn)
		msg2 = "Scan Your Hand"
		printDisplay(gameState, msg1, msg2, [], players)
		time.sleep(1)
		for k in range(5):
			if k is not 0:
				X = Cards()
				if X in players[gameState.turn-1].hand:
					msg1 = "Card Exists"
					msg2 = "Try again"
					printDisplay(gameState, msg1, msg2, [], players)
					time.sleep(1)
					k = k - 1
				else:
					players[gameState.turn-1].handAppend(X)
					msg1 = "Player {}".format(gameState.turn)
					msg2 = "Cards Scanned: {}".format(k+1)
					printDisplay(gameState, msg1, msg2, [], players)
					time.sleep(1)
			else:
				X = Cards()
				players[gameState.turn-1].handAppend(X)
				msg1 = "Player {}".format(gameState.turn)
				msg2 = "Cards Scanned: {}".format(k+1)
				printDisplay(gameState, msg1, msg2, [], players)
				time.sleep(1)
		gameState.incTurn()

def checkRenig(gameState, teams, players):
	print("CHECK RENIG")
	if gameState.trump is suitsArray[1]:
        gameState.opposite = suitsArray[3]
    elif gameState.trump is suitsArray[2]:
        gameState.opposite = suitsArray[4]
    elif gameState.trump is suitsArray[3]:
        gameState.opposite = suitsArray[1]
    elif gameState.trump is suitsArray[4]:
        gameState.opposite = suitsArray[2]
	if gameState.leadTurn is False:
		if gameState.roundHand[-1].suit is not gameState.lead:
			for i in range(len(players[gameState.turn-1].hand)):
				if players[gameState.turn-1].hand[i] is not gameState.roundHand[-1]:
					if players[gameState.turn-1].hand[i].suit is gameState.lead:
						if players[gameState.turn-1].hand[i].suit is gameState.opposite
							if players[gameState.turn-1].hand[i].val is not 'J':
								msg1 = "Team: {} renig".format(team.Name)
								msg2 = ""
								printAll(msg1, msg2, [], players)
								teams[(gameState.turn-1)%2].updateRenig(1)
								return True
						else:
							msg1 = "Team: {} renig".format(team.Name)
							msg2 = ""
							printAll(msg1, msg2, [], players)
							teams[(gameState.turn-1)%2].updateRenig(1)
							return True
	return False

def scoreRound(gameState, teams, players):
	tempVal = 0
	winner = 0
	for i in range(len(gameState.roundHand)):
		print("roundHand " + str(i) + " " + str(gameState.roundHand[i].val))
		Val = convertInt(gameState, i)
		print(str(i+1) + "Value: " + str(Val))
		if Val > tempVal:
			tempVal = Val
			winner = i

	return winner



def checkScore(gameState, teams):
	if teams[0].renig > teams[1].renig:
		teams[1].updateScore(2)
	elif  teams[1].renig > teams[0].renig:
		teams[0].updateScore(2)
	else:
		if teams[0].tricks is 5:
			if teams[0].alone is True:
				teams[0].updateScore(4)
			else:
				teams[0].updateScore(2)
		elif teams[1].tricks is 5:
			if teams[1].alone is True:
				teams[1].updateScore(4)
			else:
				teams[1].updateScore(2)
		elif teams[0].tricks >=3:
			if teams[1].called is True:
				teams[0].updateScore(2)
			else:
				teams[0].updateScore(1)
		elif teams[1].tricks >=3:
			if teams[0].called is True:
				teams[1].updateScore(2)
			else:
				teams[1].updateScore(1)

	if teams[0].score >= 10:
		gameState.updateEndGame(True)
	elif teams[1].score >=10:
		gameState.updateEndGame(True)

#def compareVal(gameState):

def convertInt(gameState, i):
	print("roundHand[i] " + str(gameState.roundHand[i].val))
	intVal = 0
	if gameState.roundHand[i].val is '9':
		intVal = 1
	elif gameState.roundHand[i].val is '10':
		intVal = 2
	elif gameState.roundHand[i].val is '11':
		intVal = 3
	elif gameState.roundHand[i].val is '12':
		intVal = 4
	elif gameState.roundHand[i].val is '13':
		intVal = 5
	elif gameState.roundHand[i].val is '14':
		intVal = 6
	print("intVal: " + str(intVal))
	return adjustVal(gameState, intVal, i)

def adjustVal(gameState, intVal, i):
	if gameState.trump is gameState.roundHand[i].suit:
		intVal = intVal + 20
		if intVal is 23:
			intVal = intVal + 10
	elif gameState.trump is suitsArray[1]:
		opp = SuitsArray[3]
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is suitsArray[2]:
		opp = suitsArray[4]
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is suitsArray[3]:
		opp = suitsArray[1]
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is suitsArray[4]:
		opp = suitsArray[2]
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.lead is gameState.roundHand[i].suit:
		intVal = intVal + 10
	else:
		intVal = intVal
	print("adjustedVal: " + str(intVal))
	return intVal

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
    for j in players[gameState.turn-1].hand:
        if players[gameState.turn-1].hand[Cards].suit is gameState.lead:
            hint = 1
            break   
        elif players[gameState.turn-1].hand[Cards].suit is gameState.trump:
            for i in gameState.roundHand:
                if gameState.roundHand[i].suit is gameState.trump:
                    if convertInt(gameState, players[gameState.turn-1].hand[Cards].val, players[gameState.turn-1].hand[Cards].suit) > convertInt(gameState, gameState.roundHand[i].val, gameState.roundHand[i].suit):
                        hint = 2           
        else:
            if hint is not 2:
				if hint is not 1:
                	hint = 0
        printHint(gameState, players, hint)

def playRound(gameState, teams, players):
	print("NOMRAL ROUND")
	gameState.setTurn(gameState.deal)
	gameState.incTurn()

	scanHands(gameState, teams, players)
	renigTest = False
	for k in range(5):
		for j in range(4):
			msg1 = "Wait..."
			msg2 = "T:* L:* A:{} B:{}".format(teams[0].score, teams[1].score)
			printAll(msg1, msg2, [], players)
			time.sleep(1)
			msg1 = "Player {} Turn".format(gameState.turn)
			msg2 = "T:* L:* A:{} B:{}".format(teams[0].score, teams[1].score)
			printDisplay(gameState, msg1, msg2, [gamState.trump. gameState.lead], players)
			time.sleep(1)

			if j is 0:
				gameState.updateLeadTurn(True)
				#print("Lead with high off suit")
				X = Cards()
				if gameState.trump is suitsArray[1]:
					gameState.opposite = suitsArray[3]
				elif gameState.trump is suitsArray[2]:
					gameState.opposite = suitsArray[4]
				elif gameState.trump is suitsArray[3]:
					gameState.opposite = suitsArray[1]
				elif gameState.trump is suitsArray[4]:
					gameState.opposite = suitsArray[2]
				if X.suit is gameState.opposite:
					if X.val is 'J':
						gameState.setLead(gameState.trump)
					else:
						gameState.setLead(X.suit)
				else:
					gameState.setLead(X.suit)
			else:
				gameState.updateLeadTurn(False)
				X = Cards()
				checkHint(gameState, teams, hands)

			gameState.updateRoundPlay(True)

			#id = input("ID: ")

			gameState.updateRoundHand(X)



			if renigTest is False:
				renigTest = checkRenig(gameState, teams, players)

			if renigTest is True:
				break

			gameState.incTurn()
			del X
		if renigTest is True:
			gameState.clearRoundHand()
			break
		size = scoreRound(gameState, teams, players)
		for i in range(size):
			gameState.incTurn()
		msg1 = "Player: {}".format(gameState.turn)
		msg2 = "Won the trick"
		printAll(msg1, msg2, [], players)

		teams[(gameState.turn-1)%2].updateTricks()
		gameState.clearRoundHand()
		print ("TeamA Tricks: " + str(teams[0].tricks))
		print ("TeamB Tricks: " + str(teams[1].tricks))
		print ("TeamA Score: " + str(teams[0].score))
		print ("TeamB Score: " + str(teams[1].score))
	checkScore(gameState, teams)
	print ("TeamA Tricks: " + str(teams[0].tricks))
	print ("TeamB Tricks: " + str(teams[1].tricks))
	print ("TeamA Score: " + str(teams[0].score))
	print ("TeamB Score: " + str(teams[1].score))
	gameState.incDeal()
	gameState.setTurn(gameState.deal)
	teams[0].clearTricks()
	teams[1].clearTricks()
	for play in range(len(players)):
		players[play].handClear()
	if gameState.endGame is True:
		if teams[0].score >= 10:
			printAll("Team A wins", "Y-Next Game", [], players)
		else:
			printAll("Team B wins", "Y-Next Game", [], players)
		while True:
	            if players[0].keypad.getResponse() is 9 or players[1].keypad.getResponse() is 9 or players[2].keypad.getResponse() is 9 or players[3].keypad.getResponse() is 9: #Y
	                time.sleep(2)
		main(gameState, teams, players)
	else:
		dealRound(gameState, teams, players)
		callPass(gameState, teams, players)

def playAlone(gameState, teams, players):
	print("GOING ALONE")
	gameState.setTurn(gameState.deal)
	gameState.incTurn()
	
	for i in range(len(players)):
		if players[i].alone is True:
			gameState.setTurn(i + 1)
			if i + 2 < 4:
				print(str(i+2) + "IS SKIPPED")
				players[i+2].updateSkip(True)
			else:
				print(str(i-2) + "IS SKIPPED")
				players[i-2].updateSkip(True)
	#print("SKIP: " + str(gameState.turn))
	#skipTest = gameState.turn
	scanHands(gameState, teams, players)
	renigTest = False

	#if skipTest is -1:
		#skipTest = 4
	#print("SKIP: " + str(skipTest))

	#gameState.setTurn(gameState.deal)

	i = 0
	for k in range(5):
		for j in range(4):
			if players[gameState.turn-1].skip is False:
				msg1 = "Wait..."
				msg2 = "T:* L:* A:{} B:{}".format(teams[0].score, teams[1].score)
				printAll(msg1, msg2, [], players)
				time.sleep(1)
				msg1 = "Player {} Turn".format(gameState.turn)
				msg2 = "T:* L:* A:{} B:{}".format(teams[0].score, teams[1].score)
				printDisplay(gameState, msg1, msg2, [gamState.trump. gameState.lead], players)
				time.sleep(1)

				if i is 0:
					gameState.updateLeadTurn(True)
					#print("Lead with high off suit")
					X = Cards()
					gameState.setLead(X.suit)
				else:
					gameState.updateLeadTurn(False)
					X = Cards()
					checkHint(gameState, teams, hands)

				gameState.updateRoundPlay(True)

				gameState.updateRoundHand(X)

				if renigTest is False:
					renigTest = checkRenig(gameState, teams, players)
				if renigTest is True:
					break

				gameState.incTurn()
				del X
				i = i + 1
			else:
				gameState.incTurn()

		if renigTest is True:
			gameState.clearRoundHand()
			break
		size = scoreRound(gameState, teams, players)
		for i in range(size):
			gameState.incTurn()
			if players[gameState.turn-1].skip is True:
				gameState.incTurn()
		msg1 = "Player: {}".format(gameState.turn)
		msg2 = "Won the trick"
		printAll(msg1, msg2, [], players)

		teams[(gameState.turn-1)%2].updateTricks()
		gameState.clearRoundHand()
		print ("TeamA Tricks: " + str(teams[0].tricks))
		print ("TeamB Tricks: " + str(teams[1].tricks))
		print ("TeamA Score: " + str(teams[0].score))
		print ("TeamB Score: " + str(teams[1].score))
	for i in range(len(players)):
		players[i].updateSkip(False)
		players[i].updateAlone(False)
	for i in range(len(teams)):
		teams[i].updateAlone(False)
	checkScore(gameState, teams)
	print ("TeamA Tricks: " + str(teams[0].tricks))
	print ("TeamB Tricks: " + str(teams[1].tricks))
	print ("TeamA Score: " + str(teams[0].score))
	print ("TeamB Score: " + str(teams[1].score))
	gameState.incDeal()
	gameState.setTurn(gameState.deal)
	teams[0].clearTricks()
	teams[1].clearTricks()
	for play in range(len(players)):
		players[play].handClear()
	if gameState.endGame is True:
		if teams[0].score >= 10:
			printAll("Team A wins", "Y-Next Game", [], players)
		else:
			printAll("Team A wins", "Y-Next Game", [], players)
		while True:
    	            if players[0].keypad.getResponse() is 9 or players[1].keypad.getResponse() is 9 or players[2].keypad.getResponse() is 9 or players[3].keypad.getResponse() is 9: #Y
	                time.sleep(2)
	        main(gameState, teams, players)

	else:
		dealRound(gameState, teams, players)
		callPass(gameState, teams, players)

def scanStart():
    uid = getUID()
    data = getData(uid)
    return suitsArray[data[3]]

def callPass(gameState, teams, deal):
    for i in range(2):
        gameState.incTurn()
        msg1 = "Wait..."
        msg2 = ""
        printAll(msg1, msg2, [], players)
        time.sleep(1)

        if i is 0:
            msg1 = "Player {} Turn".format(gameState.turn)
            msg2 = "Call(Y) Pass(N)"
            printDisplay(gameState, msg1, msg2, [], players)
            time.sleep(1)
            while True:
                resp = players[gameState.turn-1].keypad.getResponse()
                time.sleep(0.5)
                confResp = playerConfirm(gameState, msg1, msg2, [], players, resp)
                if confResp is 9:
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
                msg1 = "Call(Suit)"
                msg2 = "or Pass(N)"
                printDisplay(gameState, msg1, msg2, dummy, players)
                while True:
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
                    players[gameState.turn-1].updateAlone(True)
                    teams[(gameState.turn-1)%2].updateAlone(True)
                    playAlone(gameState, teams, players)
                else:
                    playRound(gameState, teams, players)

            else:
                gameState.incTurn()

                msg1 = "Wait..."
                msg2 = ""
                printAll(msg1, msg2, [], players)
                time.sleep(1)

                if i is 0:
                    msg1 = "Player {} Turn".format(gameState.turn)
                    msg2 = "Call(Y) Pass(N)"
                    printDisplay(gameState, msg1, msg2, [], players)
                    time.sleep(1)
                    while True:
                        resp = players[gameState.turn-1].keypad.getResponse()
                        time.sleep(0.5)
                        confResp = playerConfirm(gameState, msg1, msg2, [], players, resp)
                        if confResp is 9:
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
                    msg1 = "Call(Suit)"
                    msg2 = "or Pass(N)"
                    printDisplay(gameState, msg1, msg2, dummy, players)
                    while True:
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
                        players[gameState.turn-1].updateAlone(True)
                        teams[(gameState.turn-1)%2].updateAlone(True)
                        playAlone(gameState, teams, players)
                    else:
                        playRound(gameState, teams, players)

                else:
                    gameState.incTurn()

                    msg1 = "Wait..."
                    msg2 = ""
                    printAll(msg1, msg2, [], players)
                    time.sleep(1)

                    if i is 0:
                        msg1 = "Player {} Turn".format(gameState.turn)
                        msg2 = "Call(Y) Pass(N)"
                        printDisplay(gameState, msg1, msg2, [], players)
                        time.sleep(1)
                        while True:
                            resp = players[gameState.turn-1].keypad.getResponse()
                            time.sleep(0.5)
                            confResp = playerConfirm(gameState, msg1, msg2, [], players, resp)
                            if confResp is 9:
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
                        msg1 = "Call(Suit)"
                        msg2 = "or Pass(N)"
                        printDisplay(gameState, msg1, msg2, dummy, players)
                        while True:
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
                            players[gameState.turn-1].updateAlone(True)
                            teams[(gameState.turn-1)%2].updateAlone(True)
                            playAlone(gameState, teams, players)
                        else:
                            playRound(gameState, teams, players)

                    else:
                        gameState.incTurn()

                        msg1 = "Wait..."
                        msg2 = ""
                        printAll(msg1, msg2, [], players)
                        time.sleep(1)

                        if i is 0:
                            msg1 = "Player {} Turn".format(gameState.turn)
                            msg2 = "Call(Y) Pass(N)"
                            printDisplay(gameState, msg1, msg2, [], players)
                            time.sleep(1)
                            while True:
                                resp = players[gameState.turn-1].keypad.getResponse()
                                time.sleep(0.5)
                                confResp = playerConfirm(gameState, msg1, msg2, [], players, resp)
                                if confResp is 9:
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
                            msg1 = "Call(Suit)"
                            msg2 = ""
                            printDisplay(gameState, msg1, msg2, dummy, players)
                            while True:
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

                        if confResp is not 10: #N
                            msg1 = "Alone?(Y/n)"
                            msg2 = ""
                            printDisplay(gameState, msg1, msg2, dummy, players)

                            resp = players[gameState.turn-1].keypad.getResponse()
                            time.sleep(1)
                            confResp = playerConfirm(gameState, msg1, msg2, dummy, players, resp)

                            teams[(gameState.turn-1)%2].updateCalled(True)

                            if confResp is 9: #Y
                                players[gameState.turn-1].updateAlone(True)
                                teams[(gameState.turn-1)%2].updateAlone(True)
                                playAlone(gameState, teams, players)
                            else:
                                playRound(gameState, teams, players)
                        else:
                            gameState.incTurn()

def main(gameState, teams, players):
    initCustChars(players)
    while True:
		gameState.incDeal()
		dealRound(gameState, teams, players)
		gameState.setTurn(gameState.deal)
		callPass(gameState, teams, players)

if __name__ == '__main__':
	gameState = gameState()

	P1 = player(1, I2C_ADP1, 1)
	P2 = player(2, I2C_ADP2, 1)
	P3 = player(3, I2C_ADP3, 1)
	P4 = player(4, I2C_ADP4, 1)

	players = [P1, P2, P3, P4]

	ATeam = Team("A")
	BTeam = Team("B")
	teams = [ATeam, BTeam]

	try:
		main(gameState, teams, players)
	except KeyboardInterrupt:
		pass
	finally:
		print("KEYBOARD INTERRUPT")
		P1.lcd.lcd_byte(0x01, LCD_CMD)
    	P2.lcd.lcd_byte(0x01, LCD_CMD)
    	P3.lcd.lcd_byte(0x01, LCD_CMD)
    	P4.lcd.lcd_byte(0x01, LCD_CMD)
