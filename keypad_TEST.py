import binascii
import sys
import smbus
import time

from keypad import keypad

P1 = keypad(1)
print ("input recieved {}".format(P1.getResponse()))