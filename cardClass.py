#/usr/bin/python3

import binascii
import sys

import Adafruit_PN532 as PN532

suitsArray = ["", "hearts", "spades", "diamonds", "clubs"]
cardsList = []

CS = 'P8_7'
MOSI = 'P8_8'
MISO = 'P8_9'
SCLK = 'P8_10'

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()

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
    def __init__(self):
        self.uid = getUID()
        data = getData(self.uid)
        self.suit = suitsArray[data[3]]
        self.val = data[2]    

def main():
    print("Player 1 Hand one card at a time")

#P1Hand = [Cards() for i in range(5)]

    P1Hand = []

    for i in range(5):
        x = Cards()
        P1Hand.append(x)
        print("P1 Card {0}: {1} of {2}".format(i+1, P1Hand[i].val, P1Hand[i].suit))
        raw_input("Enter for next card")

    for i in range(5):
        print("P1 Card {0}: {1} of {2}".format(i+1, P1Hand[i].val, P1Hand[i].suit))

    print("Player 1 play a card")
    P1T1 = Cards()
    print("Player 1 played: {0} of {1} this turn".format(P1T1.val, P1Hand[i].suit))


main()
