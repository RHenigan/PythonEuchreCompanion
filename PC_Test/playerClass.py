class Player:
	def __init__(self):
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

class Team:
	def __init__(self):
		self.score = 0
		self.tricks = 0
		self.called = False
		self.renig = 0
		self.alone = False

	def resetScore(self):
		self.score = 0

	def resetTricks(self):
		self.tricks = 0

	def updateScore(self, val):
		self.score = self.score + val

	def updateTricks(self):
		self.tricks = self.tricks + 1

	def clearTricks(self):
		self.tricks = 0

	def updateCalled(self, flag):
		self.called = flag

	def updateAlone(self, flag):
		self.alone = flag

	def updateRenig(self, val):
		self.renig = val

class gameState:
	def __init__(self):
		self.roundPlay = False
		self.leadTurn = False
		self.turn = 0
		self.deal = 0
		self.roundHand = []
		self.lead = 'X'
		self.trump = 'X'
		self.endGame = False

	def updateEndGame(self, flag):
		self.endGame = flag

	def updateRoundPlay(self, flag):
		self.roundPlay = flag

	def updateLeadTurn(self, flag):
		self.leadTurn = flag

	def updateRoundHand(self, card):
		self.roundHand.append(card)

	def clearRoundHand(self):
		self.roundHand = []

	def setTurn(self, player):
		self.turn = player

	def setDeal(self, player):
		self.deal = player

	def incTurn(self):
		if self.turn > 3:
			self.turn = 1
		else:
			self.turn = self.turn + 1
	
	def incDeal(self):
		if self.deal > 3:
			self.deal = 1
		else:
			self.deal = self.deal + 1

	def setTrump(self, suit):
		self.trump = suit

	def setLead(self, suit):
		self.lead = suit