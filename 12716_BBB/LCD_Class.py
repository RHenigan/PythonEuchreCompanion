#!/usr/bin/python
import smbus
import time

#define screen size and addr
I2C_ADP1  = 0x3f # I2C device address
I2C_ADP2  = 0x3e # I2C device address
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


#Generic i2c class
class i2c_device:
    def __init__ (self, addr, port):
        self.addr = addr
        self.bus = smbus.SMBus(port)
        
    def write(self, byte):
        self.bus.write_byte(self.addr, byte)
        
    def read(self):
        return self.bus.read_byte(self.addr)
        
    def read_nbytes_data(self, data, n):
        return self.bus.read_i2c_blockdata(self.addr, data, n)
        
        
class lcd:
    def __init__ (self, addr, port):
        #create i2c obj
        self.lcd_device = i2c_device(addr, port)
        # Initialise display
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD) # 000001 Clear display
        time.sleep(E_DELAY)
    
    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        self.lcd_device.write(bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.lcd_device.write(bits_low)
        self.lcd_toggle_enable(bits_low)
        
    def custom_char(self, custom, location):
        assert 0 <= location <= 7, 'Only locations 0-7 are valid.'
        assert len(custom) == 8, 'Bitmap should have exactly 8 rows.'
        
        self.lcd_byte((0x40 | location << 3), LCD_CMD)
        
        for row in custom:
            self.lcd_byte(row, LCD_CHR)
        
        
    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(E_DELAY)
        self.lcd_device.write((bits | ENABLE))
        time.sleep(E_PULSE)
        self.lcd_device.write((bits & ~ENABLE))
        time.sleep(E_DELAY)
    
    def lcd_string(self, message, line):
        # Send string to display

        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)
            
    
    #TODO remake or make another custom string            
    def lcd_custom_str(self, message, list, line):
        # Send string to display

        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line, LCD_CMD)

        j = 0
        for i in range(LCD_WIDTH):
            if message[i] is "*":
                self.lcd_byte(ord(list[j]), LCD_CHR)
                j = j+1
            else:
                self.lcd_byte(ord(message[i]), LCD_CHR)
