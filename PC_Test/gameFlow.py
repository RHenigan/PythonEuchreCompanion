from cardClass import Cards
from playerClass import Player
from playerClass import Team
from playerClass import gameState

import time
import sys

#TODO renig flag setting, adapt to HW

dummy = []

def dealRound(gameState, teams, players):
	print("Player " + str(gameState.deal) + " deal cards")
	input("Enter To Finish Deal")

def scanHands(gameState, teams, players):
	for num in range(len(players)):
		print("Player " + str(gameState.turn) + " scan your hand")
		for k in range(5):
			if k is not 0:
				id = input("ID: ")
				suit = input("SUIT: ")
				val = input("VAL: ")
				Y = Cards(int(id), int(val), suit)
				if Y in players[gameState.turn-1].hand:
					print("Card exists in hand")
					k = k - 1
				else:
					X = Cards(int(id), int(val), suit)
					players[gameState.turn-1].handAppend(X)
					print("Player " + str(gameState.turn) + " cards scanned: " + str(k+1))
			else:
				id = input("ID: ")
				suit = input("SUIT: ")
				val = input("VAL: ")
				X = Cards(int(id), int(val), suit)
				players[gameState.turn-1].handAppend(X)
				print("Player " + str(gameState.turn) + " cards scanned: " + str(k+1))
		print ("Player " + str(gameState.turn) + " hand")
		for i in range(len(players[gameState.turn - 1].hand)):
		    print(str(players[gameState.turn - 1].hand[i].val) + str(players[gameState.turn - 1].hand[i].suit))
		gameState.incTurn()

def checkRenig(gameState, teams, players):
	print("CHECK RENIG")
	if gameState.leadTurn is False:
		if gameState.roundHand[-1].suit is not gameState.lead:
			for i in range(len(players[gameState.turn-1].hand)):
				if players[gameState.turn-1].hand[i] is not gameState.roundHand[-1]:
					if players[gameState.turn-1].hand[i].suit is gameState.lead:
						print("Team: " + str((gameState.turn-1)%2) + " renig")
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
	if gameState.roundHand[i].val is 9:
		intVal = 1
	elif gameState.roundHand[i].val is 10:
		intVal = 2
	elif gameState.roundHand[i].val is 11:
		intVal = 3
	elif gameState.roundHand[i].val is 12:
		intVal = 4
	elif gameState.roundHand[i].val is 13:
		intVal = 5
	elif gameState.roundHand[i].val is 14:
		intVal = 6
	print("intVal: " + str(intVal))
	return adjustVal(gameState, intVal, i)

def adjustVal(gameState, intVal, i):
	if gameState.trump is gameState.roundHand[i].suit:
		intVal = intVal + 20
		if intVal is 23:
			intVal = intVal + 10
	elif gameState.trump is 'H':
		opp = 'D'
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is 'S':
		opp = 'C'
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is 'D':
		opp = 'H'
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.trump is 'C':
		opp = 'S'
		if opp is gameState.roundHand[i].suit:
			if intVal is 3:
				intVal = intVal + 25
	elif gameState.lead is gameState.roundHand[i].suit:
		intVal = intVal + 10
	else:
		intVal = intVal
	print("adjustedVal: " + str(intVal))
	return intVal


def playRound(gameState, teams, players):
	print("NOMRAL ROUND")
	gameState.setTurn(gameState.deal)
	gameState.incTurn()

	scanHands(gameState, teams, players)
	renigTest = False
	for k in range(5):
		for j in range(4):
			print("Player " + str(gameState.turn) + " card for turn")

			if j is 0:
				gameState.updateLeadTurn(True)
				print("Lead with high off suit")
				id = input("ID: ")
				suit = input("SUIT: ")
				val = input("VAL: ")
				gameState.setLead(suit)
			else:
				gameState.updateLeadTurn(False)
				id = input("ID: ")
				suit = input("SUIT: ")
				val = input("VAL: ")
				#checkHint(gameState, teams, hands)

			gameState.updateRoundPlay(True)

			#id = input("ID: ")

			X = Cards(int(id), int(val), suit)
			gameState.updateRoundHand(X)



			if renigTest is False:
				renigTest = checkRenig(gameState, teams, players)

			if renigTest is True:
				break

			gameState.incTurn()
		if renigTest is True:
			gameState.clearRoundHand()
			break
		size = scoreRound(gameState, teams, players)
		for i in range(size):
			gameState.incTurn()
		print("WINNER " + str(gameState.turn))

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
			print("Team A wins")
		else:
			print("Team B wins")
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
				print("Player " + str(gameState.turn) + " card for turn")

				if i is 0:
					gameState.updateLeadTurn(True)
					print("Lead with high off suit")
				else:
					gameState.updateLeadTurn(False)
					#checkHint(gameState, teams, hands)

				gameState.updateRoundPlay(True)

				id = input("ID: ")
				suit = input("SUIT: ")
				val = input("VAL: ")

				X = Cards(int(id), int(val), suit)
				gameState.updateRoundHand(X)

				if renigTest is False:
					renigTest = checkRenig(gameState, teams, players)
				if renigTest is True:
					break

				gameState.incTurn()
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
		print("WINNER " + str(gameState.turn))

		teams[(gameState.turn-1)%2].updateTricks()
		gameState.clearRoundHand()
		print ("TeamA Tricks: " + str(teams[0].tricks))
		print ("TeamB Tricks: " + str(teams[1].tricks))
		print ("TeamA Score: " + str(teams[0].score))
		print ("TeamB Score: " + str(teams[1].score))
	for i in range(len(players)):
			players[i].updateSkip(False)
			players[i].updateAlone(False)
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
			print("Team A wins")
		else:
			print("Team B wins")
	dealRound(gameState, teams, players)
	callPass(gameState, teams, players)

def callPass(gameState, teams, deal):
	for i in range(2):
		gameState.incTurn()

		if i is 0:
			resp = input("Player " + str(gameState.turn) +" Call (1) or Pass(2)")
			if int(resp) is 1:
				print("FRIST PICK UP")
				print("Card picked up")
				resp = input("Select Trump suit(H(4), S(5), D(6), C(7))")
				if int(resp) is 4:
					gameState.setTrump('H')
					print("Trump is " + gameState.trump)
				elif int(resp) is 5:
					gameState.setTrump('S')
					print("Trump is " + gameState.trump)
				elif int(resp) is 6:
					gameState.setTrump('D')
					print("Trump is " + gameState.trump)
				elif int(resp) is 7:
					gameState.setTrump('C')
					print("Trump is " + gameState.trump)
		else:
			resp = input("Player " + str(gameState.turn) + " suit(H(4), S(5), D(6), C(7)) or pass (2)")
			if int(resp) is 4:
				gameState.setTrump('H')
				print("Trump is " + gameState.trump)
			elif int(resp) is 5:
				gameState.setTrump('S')
				print("Trump is " + gameState.trump)
			elif int(resp) is 6:
				gameState.setTrump('D')
				print("Trump is " + gameState.trump)
			elif int(resp) is 7:
				gameState.setTrump('C')
				print("Trump is " + gameState.trump)


		if int(resp) is not 2:
			resp = input("Alone Y(1) or N(2)")
			teams[(gameState.turn-1)%2].updateCalled(True)
			if int(resp) is 1:
				players[gameState.turn - 1].updateAlone(True)
				teams[(gameState.turn-1)%2].updateAlone(True)
				playAlone(gameState, teams, players)
			else:
				playRound(gameState, teams, players)

		else:
			gameState.incTurn()

			if i is 0:
				resp = input("Player " + str(gameState.turn) +" Call (1) or Pass(2)")
				if int(resp) is 1:
					print("FRIST PICK UP")
					print("Card picked up")
					resp = input("Select Trump suit(H(4), S(5), D(6), C(7))")
					if int(resp) is 4:
						gameState.setTrump('H')
						print("Trump is " + gameState.trump)
					elif int(resp) is 5:
						gameState.setTrump('S')
						print("Trump is " + gameState.trump)
					elif int(resp) is 6:
						gameState.setTrump('D')
						print("Trump is " + gameState.trump)
					elif int(resp) is 7:
						gameState.setTrump('C')
						print("Trump is " + gameState.trump)
			else:
				resp = input("Player " + str(gameState.turn) + " suit(H(4), S(5), D(6), C(7)) or pass (2)")
				if int(resp) is 4:
					gameState.setTrump('H')
					print("Trump is " + gameState.trump)
				elif int(resp) is 5:
					gameState.setTrump('S')
					print("Trump is " + gameState.trump)
				elif int(resp) is 6:
					gameState.setTrump('D')
					print("Trump is " + gameState.trump)
				elif int(resp) is 7:
					gameState.setTrump('C')
					print("Trump is " + gameState.trump)


			if int(resp) is not 2:
				resp = input("Alone Y(1) or N(2)")
				teams[(gameState.turn-1)%2].updateCalled(True)
				if int(resp) is 1:
					players[gameState.turn - 1].updateAlone(True)
					teams[(gameState.turn-1)%2].updateAlone(True)
					playAlone(gameState, teams, players)
				else:
					playRound(gameState, teams, players)

			else:
				gameState.incTurn()

				if i is 0:
					resp = input("Player " + str(gameState.turn) +" Call (1) or Pass(2)")
					if int(resp) is 1:
						print("FRIST PICK UP")
						print("Card picked up")
						resp = input("Select Trump suit(H(4), S(5), D(6), C(7))")
						if int(resp) is 4:
							gameState.setTrump('H')
							print("Trump is " + gameState.trump)
						elif int(resp) is 5:
							gameState.setTrump('S')
							print("Trump is " + gameState.trump)
						elif int(resp) is 6:
							gameState.setTrump('D')
							print("Trump is " + gameState.trump)
						elif int(resp) is 7:
							gameState.setTrump('C')
							print("Trump is " + gameState.trump)
				else:
					resp = input("Player " + str(gameState.turn) + " suit(H(4), S(5), D(6), C(7)) or pass (2)")
					if int(resp) is 4:
						gameState.setTrump('H')
						print("Trump is " + gameState.trump)
					elif int(resp) is 5:
						gameState.setTrump('S')
						print("Trump is " + gameState.trump)
					elif int(resp) is 6:
						gameState.setTrump('D')
						print("Trump is " + gameState.trump)
					elif int(resp) is 7:
						gameState.setTrump('C')
						print("Trump is " + gameState.trump)


				if int(resp) is not 2:
					resp = input("Alone Y(1) or N(2)")
					teams[(gameState.turn-1)%2].updateCalled(True)
					if int(resp) is 1:
						players[gameState.turn - 1].updateAlone(True)
						teams[(gameState.turn-1)%2].updateAlone(True)
						playAlone(gameState, teams, players)
					else:
						playRound(gameState, teams, players)

				else:
					gameState.incTurn()

					if i is 0:

						resp = input("Player " + str(gameState.turn) +" Call (1) or Pass(2)")
						if int(resp) is 1:
							print("FRIST PICK UP")
							print("Card picked up")
							resp = input("Select Trump suit(H(4), S(5), D(6), C(7))")
							if int(resp) is 4:
								gameState.setTrump('H')
								print("Trump is " + gameState.trump)
							elif int(resp) is 5:
								gameState.setTrump('S')
								print("Trump is " + gameState.trump)
							elif int(resp) is 6:
								gameState.setTrump('D')
								print("Trump is " + gameState.trump)
							elif int(resp) is 7:
								gameState.setTrump('C')
								print("Trump is " + gameState.trump)
					else:
						while True:
							resp = input("Player " + str(gameState.turn) + " suit(H(4), S(5), D(6), C(7))")
							if int(resp) is 4:
								gameState.setTrump('H')
								print("Trump is " + gameState.trump)
								break
							elif int(resp) is 5:
								gameState.setTrump('S')
								print("Trump is " + gameState.trump)
								break
							elif int(resp) is 6:
								gameState.setTrump('D')
								print("Trump is " + gameState.trump)
								break
							elif int(resp) is 7:
								gameState.setTrump('C')
								print("Trump is " + gameState.trump)
								break

						if int(resp) is not 2:
							resp = input("Alone Y(1) or N(2)")
							teams[(gameState.turn-1)%2].updateCalled(True)
							if int(resp) is 1:
								players[gameState.turn - 1].updateAlone(True)
								teams[(gameState.turn-1)%2].updateAlone(True)
								playAlone(gameState, teams, players)
							else:
								playRound(gameState, teams, players)
						else:
							gameState.incTurn()

def main(gameState, teams, players):
	while True:
		gameState.incDeal()
		dealRound(gameState, teams, players)
		gameState.setTurn(gameState.deal)
		callPass(gameState, teams, players)

if __name__ == '__main__':
	gameState = gameState()

	P1 = Player()
	P2 = Player()
	P3 = Player()
	P4 = Player()

	players = [P1, P2, P3, P4]

	ATeam = Team()
	BTeam = Team()
	teams = [ATeam, BTeam]

	try:
		main(gameState, teams, players)
	except KeyboardInterrupt:
		pass
	finally:
		print("KEYBOARD INTERRUPT")