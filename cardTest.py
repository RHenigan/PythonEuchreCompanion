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


def main():
	print("Scan all cards, one at a time")
	Deck = []
	raw_input("Enter for next card")

	for i in range(24):
        #create new card
        x = Cards()
        Deck.append(x)
        print("{}{} was played".format(Deck[i].suit, Deck[i].val))
        raw_input("Enter for next card")

if __name__ == '__main__':
	try:
        main()
    except KeyboardInterrupt:
        pass