import binascii
import sys
import smbus
import time

from cardClass import Cards
from LCD_Class import lcd
from LCD_Class import i2c_device
from keypad import keypad

#heart, spade, diamond, club
suitsArray = [unichr(0), unichr(0), unichr(1), unichr(2), unichr(3)]

#define screen width and i2c addr
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
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
#bus = smbus.SMBus(1) # Rev 2 Pi uses 1

#define custom chars
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
def initCustChars(P1Disp, P2Disp, P3Disp, P4Disp):
    P1Disp.custom_char(heartChar, 0)
    P1Disp.custom_char(spadeChar, 1)
    P1Disp.custom_char(diamondChar, 2)
    P1Disp.custom_char(clubChar, 3)
    P2Disp.custom_char(heartChar, 0)
    P2Disp.custom_char(spadeChar, 1)
    P2Disp.custom_char(diamondChar, 2)
    P2Disp.custom_char(clubChar, 3)
    P3Disp.custom_char(heartChar, 0)
    P3Disp.custom_char(spadeChar, 1)
    P3Disp.custom_char(diamondChar, 2)
    P3Disp.custom_char(clubChar, 3)
    P4Disp.custom_char(heartChar, 0)
    P4Disp.custom_char(spadeChar, 1)
    P4Disp.custom_char(diamondChar, 2)
    P4Disp.custom_char(clubChar, 3)



def main(P1Disp, P2Disp, P3Disp, P4Disp):
    #init keypads
    #P1keypad = keypad(1)
    
    #init custom chars
    initCustChars(P1Disp, P2Disp, P3Disp, P4Disp)

    print("Scan all cards, one at a time")
    
    #empty array to hold cards
    Deck = []

    #response interface
    #P1keypad.setTurn()
    #P1keypad.setDeal()
    #charResponse = P1keypad.getResponse()
    
    #P1Disp.lcd_custom_str("* was selected", [charResponse], LCD_LINE_1)
    #P2Disp.lcd_custom_str("* was selected", [charResponse], LCD_LINE_1)
    #P3Disp.lcd_custom_str("* was selected", [charResponse], LCD_LINE_1)
    #P4Disp.lcd_custom_str("* was selected", [charResponse], LCD_LINE_1)
    

    #wait for user to press enter
    raw_input("Enter for next card")

    #normal LCD print statements
    P1Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
    P2Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
    P3Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
    P4Disp.lcd_string("Waiting for card ...", LCD_LINE_1)

    #read for all 24 cards
    for i in range(24):
        #create new card
        x = Cards()
        Deck.append(x)
        
        #print card val and suit using lcd custom print
        P1Disp.lcd_custom_str("** Was Played", [Deck[i].val, Deck[i].suit], LCD_LINE_1)
        P1Disp.lcd_string("Press Enter ...",LCD_LINE_2)
        P2Disp.lcd_custom_str("** Was Played", [Deck[i].val, Deck[i].suit], LCD_LINE_1)
        P2Disp.lcd_string("Press Enter ...",LCD_LINE_2)
        P3Disp.lcd_custom_str("** Was Played", [Deck[i].val, Deck[i].suit], LCD_LINE_1)
        P3Disp.lcd_string("Press Enter ...",LCD_LINE_2)
        P4Disp.lcd_custom_str("** Was Played", [Deck[i].val, Deck[i].suit], LCD_LINE_1)
        P4Disp.lcd_string("Press Enter ...",LCD_LINE_2)
        
        #wait for user to press enter
        raw_input("Enter for next card")
        
        #clear displays
        P1Disp.lcd_byte(0x01, LCD_CMD)
        P2Disp.lcd_byte(0x01, LCD_CMD)
        P3Disp.lcd_byte(0x01, LCD_CMD)
        P4Disp.lcd_byte(0x01, LCD_CMD)
        
        #update displays
        P1Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
        P2Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
        P3Disp.lcd_string("Waiting for card ...", LCD_LINE_1)
        P4Disp.lcd_string("Waiting for card ...", LCD_LINE_1)


if __name__ == '__main__':
    
    #initialize displays
    P1Disp = lcd(I2C_ADP1, 1)
    P2Disp = lcd(I2C_ADP2, 1)
    P3Disp = lcd(I2C_ADP3, 1)
    P4Disp = lcd(I2C_ADP4, 1)

    try:
        main(P1Disp, P2Disp, P3Disp, P4Disp)
    except KeyboardInterrupt:
        pass
    finally:
        P1Disp.lcd_byte(0x01, LCD_CMD)
        P2Disp.lcd_byte(0x01, LCD_CMD)
        P3Disp.lcd_byte(0x01, LCD_CMD)
        P4Disp.lcd_byte(0x01, LCD_CMD)
