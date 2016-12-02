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
	def __init__(self):
		self.score = 0
		self.tricks = 0
		self.Called = False
		self.Alone = False

	def updateCalled(self, val):
		self.Called = self.score + val

	def updateAlone(self, val):
		self.Alone = self.score + val

	def updateScore(self, val):
		self.score = self.score + val

	def resetScore(self):
		self.score = 0

	def updateTricks(self):
		self.tricks = self.tricks+1

	def resetTricks(self):
		self.tricks = 0

class player:
	def __init__(self, player, addr, port):
		self.lcd = lcd(addr, port)
		self.keypad = keypad(player)
		self.hand = []

	def handAppend(self, card):
		self.hand.append(card)

	def handClear(self):
		self.hand = []

class gameState:
	def __init__(self):
		self.roundPlay = False
		self.leadTurn = False
		self.turn = 1
		self.deal = 1
		self.roundHand = []
		self.lead = suitsArray[0]
		self.trump = suitsArray[0]
		self.renigA = False
		self.renigB = False
		self.endGame = False
		self.opposite = suitsArray[0]

	def setEndGame(self, boolTag):
		self.endGame = boolTag

	def setRoundPlay(self, boolTag):
		self.roundPlay = boolTag

	def setleadTurn(self, boolTag):
		self.leadTurn = boolTag

	def updateRoundHand(self, card):
		self.roundHand.append(card)

	def clearRoundHand(self):
		self.roundHand = []

	def setTurn(self, player):
		self.turn = player

	def incTurn(self):
		self.turn = self.turn + 1
		if self.turn > 1:
			self.turn = 1

	def incDeal(self):
		self.deal = self.deal + 1
		if self.deal > 1:
			self.deal = 1

	def setTrump(self, suit):
		self.trump = suit

	def setLead(self, suit):
		self.lead = suit




