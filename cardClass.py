#/usr/bin/python3

import binascii
import sys

import Adafruit_PN532 as PN532
#heart, spade, diamond, club
suitsArray = [unichr(0), unichr(0), unichr(1), unichr(2), unichr(3)]

#pins
CS = 'P8_7'
MOSI = 'P8_8'
MISO = 'P8_9'
SCLK = 'P8_10'

#initialize reader
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

#start reader
pn532.begin()

#get version
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

#configure
pn532.SAM_configuration()


#get cards unique ID
def getUID():
    print("Reading UID.....")
    while True:
        uid = pn532.read_passive_target()
        
        if uid is not None:
            print("UID Read succesful")
            return uid

#get cards data
def getData(uid):
    #default card val to 0
    cardVal = '0'
    print("Reading Data.....")
    while True:
        if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
            print("Failed to authenticate block 4!")
        
        data = pn532.mifare_classic_read_block(4)

        if data is not None:
            #return data as an array data[2] = val data[3] = suit
            print("data read successful")
            return data
        else:
            #else try again
            uid = getUID()
    
class Cards():
    #initialize a card
    def __init__(self):
        #get uid
        self.uid = getUID()
        #get data
        data = getData(self.uid)
        #get suit
        self.suit = suitsArray[data[3]]
        #get card val
        self.val = '0'
        if data[2] is 9:
            self.val = '9'
        if data[2] is 10:
            self.val = 'T'
        if data[2] is 11:
            self.val = 'J'
        if data[2] is 12:
            self.val = 'Q'
        if data[2] is 13:
            self.val = 'K'
        if data[2] is 14:
            self.val = 'A'
