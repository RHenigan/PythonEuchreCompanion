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

suitsArray = [unichr(0), unichr(0), unichr(1), unichr(2), unichr(3)]

class Team:
	def __init__(self, name):
		self.score = 0
		self.tricks = 0
		self.called = False
		self.alone = False
		self.name = name
		self.renig = 0


	def updateCalled(self, flag):
		self.called = flag

	def updateAlone(self, flag):
		self.alone = flag

	def updateScore(self, val):
		self.score = self.score + val

	def resetScore(self):
		self.score = 0

	def updateTricks(self):
		self.tricks = self.tricks+1

	def clearTricks(self):
		self.tricks = 0

	def updateRenig(self, val):
		self.renig = val

class player:
	def __init__(self, player, addr, port):
		self.lcd = lcd(addr, port)
		self.keypad = keypad(player)
		self.hand = []
		self.alone = False
		self.skip = False

	def handAppend(self, card):
		self.hand.append(card)

	def handClear(self):
		self.hand = []

	def updateAlone(self, flag):
		self.alone = flag

	def updateSkip(self, flag):
		self.skip = flag

class gameState:
	def __init__(self):
		self.roundPlay = False
		self.leadTurn = False
		self.turn = 0
		self.deal = 0
		self.roundHand = []
		self.lead = suitsArray[0]
		self.trump = suitsArray[0]
		self.endGame = False

	def updateEndGame(self, boolTag):
		self.endGame = boolTag

	def updateRoundPlay(self, boolTag):
		self.roundPlay = boolTag

	def updateLeadTurn(self, boolTag):
		self.leadTurn = boolTag

	def updateRoundHand(self, card):
		self.roundHand.append(card)

	def clearRoundHand(self):
		self.roundHand = []

	def setTurn(self, player):
		self.turn = player

	def setDeal(self, player):
		self.deal = player

	def incTurn(self):
		self.turn = self.turn + 1
		if self.turn > 4:
			self.turn = 1

	def incDeal(self):
		self.deal = self.deal + 1
		if self.deal > 4:
			self.deal = 1

	def setTrump(self, suit):
		self.trump = suit

	def setLead(self, suit):
		self.lead = suit



