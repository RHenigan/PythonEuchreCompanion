#!/usr/python
#main gameplay/rules

import binascii
import sys

import Adafruit_PN532 as PN532

#declarations
suitsArray = ["", "hearts", "spades", "diamonds", "clubs"]
cardsList = []
temp = []
P1Hand = []
P2Hand = []
P3Hand = []
P4Hand = []
i = 1

cards()

CS = 'P8_7'
MOSI = 'P8_8'
MISO = 'P8_9'
SCLK = 'P8_10'

pn532 = PN532.PN532(cs = CS, sclk=SCLK, mosi=MOSI, miso=MISO)

pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
print('BEGIN GAME')

pn532.SAM_configuration()

def scan():
        #SCANS card
        uid = getUID()
        data = getData(uid)
        x = Cards(uid, data[2], suitsArray[data[3]])
        temp.append(x)

def appendHand()
    z = temp[0]
    temp.remove(x)
    if i = 1:
        P1Hand.append(z)
    else if i = 2:
        P2Hand.append(z)
    else if i = 3:
        P3Hand.append(z)
    else: 
        P4Hand.append(z)

def checkDups(uid):
    if uid in cardsList:
        print("card exists")
        return True
    else:
        print("new card read")
        cardsList.append(uid)
        return False

def getUID():
    print("Reading UID.....")
    while True:
        uid = pn532.read_passive_target()
        
        if uid is not None:
            if checkDups(uid) is False:
                print("UID Read succesful")
                return uid

def getData(uid):
    print("Reading Data.....")
    while True:
        if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
            print("Failed to authenticate block 4!")
        
        data = pn532.mifare_classic_read_block(4)

        if data is not None:
            print("data read successful")
            return data

class Cards():
    def __init__(self, uid, val, suit):
        self.uid = uid
        self.suit = suit
        self.val = val  
    def retUID():
        return self.uid

def player(i):
    if i < 4:
        i+= 1
    else:
        i = 1 #increasing values to allow players to be dynamic

def readKey():
        #read keypad press
        
def assignVal():
#write to card - value of card

def renig():
#check suit against lead suit
#compare lead suit with the rest of the cards in hand
#if lead suit exists, tell player to scan proper card

def compare():
#compares suit and value of two cards

def printPlayer():
        

def printAll():
        

def score():

#main game
def main():
    #begin loop
    #default player 1 deal
    print("PLAYER " i " DEAL")

    for num in range(0,4)
            #Players SCAN cards
            printPlayer("PLAYER " i " SCAN CARDS")
            for k in range(5)
                scan()
                appendHand()
                print("Card {0} Recorded".format(k + 1))
                #print("P1 Card {0}: {1} of {2}".format(i+1, P1Hand[i].val, P1Hand[i].suit))
                #raw_input("Enter for next card")
        
            for j in range(5):
                print("P" j " Card {0}: {1} of {2}".format(j+1, P1Hand[j].val, P1Hand[j].suit))

            cardsList[:] = []
            player(i)
    
   #place turns in loop, check score. If score = 10, exit loop

    #default Player 1 leads deal
    print("PLAYER " i " SCAN CARD IN QUESTION")
    #Dealer SCAN the card

    #Player 2, call/pass
            #if call callTrump() playRound()
            #else Player 3, call/pass
                    #if call callTrump() playRound()
                    #else Player 4, call/pass
                            #if call callTrump() playRound()
                            #else 'screw the dealer'
                            player(i)
                            printPlayer("DEALER.. CALL TRUMP")
                            #Player 1 keypad press to call trump
                            #Assign trump
    
    player(i)
    printPlayer("PLAYER " i " TURN")
    #Player 2 lead - SCAN
    #Assign lead
    #player card values for round conditions

    printAll("PLAYER " i " TURN")
    #Player 3 play - SCAN
    #check if renig
    player(i)
    printAll("PLAYER " i " TURN")
    #Player 4 play - SCAN
    #check if renig
    player(i)
    printAll("PLAYER " i " TURN")
    #Player 1 play - SCAN
    #check if renig
    player(i)

    #SCORE ROUND
    score()


    player(i) #reassign before the next loop/round
    #loop
