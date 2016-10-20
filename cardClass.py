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
    
class Cards():
    #initialize a card
    def __init__(self):
        #get data and UID
        self.getUID()
        self.getData()
        #get suit
        self.suit = suitsArray[self.data[3]]
        #get card val
        if self.data[2] is 9:
            self.val = '9'
        elif self.data[2] is 10:
            self.val = 'T'
        elif self.data[2] is 11:
            self.val = 'J'
        elif self.data[2] is 12:
            self.val = 'Q'
        elif self.data[2] is 13:
            self.val = 'K'
        elif self.data[2] is 14:
            self.val = 'A'
        else:
            self.val = '0'
            
    #get cards unique ID
    def getUID(self):
        print("Reading UID.....")
        while True:
            Tempuid = pn532.read_passive_target()
        
            if Tempuid is not None:
                print("UID Read succesful")
                self.uid = Tempuid
                return
                
    #get cards data
    def getData(self):
        print("Reading Data.....")
        while True:
            if not pn532.mifare_classic_authenticate_block(self.uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
                print("Failed to authenticate block 4!")
        
            Tempdata = pn532.mifare_classic_read_block(4)

            if Tempdata is not None:
                #return data as an array data[2] = val data[3] = suit
                print("data read successful")
                self.data = Tempdata
                return
            else:
                self.getUID()
            
            
            
            
            
            
            
        
