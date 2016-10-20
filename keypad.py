import Adafruit_BBIO.GPIO as GPIO

#TODO avoid using predesignated pins
GPIO.setup("P8_11", GPIO.OUT)                             #Clock
GPIO.setup("P8_12", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P1 X
GPIO.setup("P8_13", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_14", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_15", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P2 X
GPIO.setup("P8_16", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_17", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_18", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P3 X
GPIO.setup("P8_19", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_20", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_21", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P4 X
GPIO.setup("P8_22", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_23", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_24", GPIO.OUT)                             #P1 Turn
GPIO.setup("P8_25", GPIO.OUT)                             #P2 Turn
GPIO.setup("P8_26", GPIO.OUT)                             #P3 Turn
GPIO.setup("P8_27", GPIO.OUT)                             #P4 Turn
GPIO.setup("P8_28", GPIO.OUT)                             #P1 Deal
GPIO.setup("P8_29", GPIO.OUT)                             #P2 Deal
GPIO.setup("P8_30", GPIO.OUT)                             #P3 Deal
GPIO.setup("P8_31", GPIO.OUT)                             #P4 Deal

#Player 1 ans
P1Ans = ["P8_12", "P8_13", "P8_14"]
#Player 2 Col
P2Ans = ["P8_15", "P8_16", "P8_17"]
#Player 3 Col
P3Ans = ["P8_18", "P8_19", "P8_20"]
#Player 4 Col
P4Ans = ["P8_21", "P8_22", "P8_23"]

#Turn LED Indicator
turnIndicator = ["P8_24", "P8_25", "P8_26", "P8_27"]
#Deal LED Indicator
dealIndicator = ["P8_28", "P8_29", "P8_30", "P8_31"]

#heart, spade, diamond, club
suitsArray = [unichr(0), unichr(0), unichr(1), unichr(2), unichr(3)]

class keypad():
    def __init__(self, player):
        self.PlayerSel = player
        self.getPlayer()

    def getPlayer(self):
        if self.PlayerSel is 1:
            self.activePlayer =  P1Ans
            return
        elif self.PlayerSel is 2:
            self.activePlayer =  P2Ans
            return
        elif self.PlayerSel is 3:
            self.activePlayer =  P3Ans
            return
        elif self.PlayerSel is 4:
            self.activePlayer =  P4Ans
            return
        else:
            print 'no player selected'
            self.activePlayer =  0
            return
            
    def setTurn(self):
        if self.PlayerSel is 1:
            GPIO.output(turnIndicator[0], GPIO.HIGH)
            GPIO.output(turnIndicator[1], GPIO.LOW)
            GPIO.output(turnIndicator[2], GPIO.LOW)
            GPIO.output(turnIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 2:
            GPIO.output(turnIndicator[0], GPIO.LOW)
            GPIO.output(turnIndicator[1], GPIO.HIGH)
            GPIO.output(turnIndicator[2], GPIO.LOW)
            GPIO.output(turnIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 3:
            GPIO.output(turnIndicator[0], GPIO.LOW)
            GPIO.output(turnIndicator[1], GPIO.LOW)
            GPIO.output(turnIndicator[2], GPIO.HIGH)
            GPIO.output(turnIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 4:
            GPIO.output(turnIndicator[0], GPIO.LOW)
            GPIO.output(turnIndicator[1], GPIO.LOW)
            GPIO.output(turnIndicator[2], GPIO.LOW)
            GPIO.output(turnIndicator[3], GPIO.HIGH)
            return
        else:
            GPIO.output(turnIndicator[0], GPIO.LOW)
            GPIO.output(turnIndicator[1], GPIO.LOW)
            GPIO.output(turnIndicator[2], GPIO.LOW)
            GPIO.output(turnIndicator[3], GPIO.LOW)
            return

    def setDeal(self):
        if self.PlayerSel is 1:
            GPIO.output(dealIndicator[0], GPIO.HIGH)
            GPIO.output(dealIndicator[1], GPIO.LOW)
            GPIO.output(dealIndicator[2], GPIO.LOW)
            GPIO.output(dealIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 2:
            GPIO.output(dealIndicator[0], GPIO.LOW)
            GPIO.output(dealIndicator[1], GPIO.HIGH)
            GPIO.output(dealIndicator[2], GPIO.LOW)
            GPIO.output(dealIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 3:
            GPIO.output(dealIndicator[0], GPIO.LOW)
            GPIO.output(dealIndicator[1], GPIO.LOW)
            GPIO.output(dealIndicator[2], GPIO.HIGH)
            GPIO.output(dealIndicator[3], GPIO.LOW)
            return
        elif self.PlayerSel is 4:
            GPIO.output(dealIndicator[0], GPIO.LOW)
            GPIO.output(dealIndicator[1], GPIO.LOW)
            GPIO.output(dealIndicator[2], GPIO.LOW)
            GPIO.output(dealIndicator[3], GPIO.HIGH)
            return
        else:
            GPIO.output(dealIndicator[0], GPIO.LOW)
            GPIO.output(dealIndicator[1], GPIO.LOW)
            GPIO.output(dealIndicator[2], GPIO.LOW)
            GPIO.output(dealIndicator[3], GPIO.LOW)
            return
            
    def getResponse(self):
        print 'get response called'
        #Get active player
        X = GPIO.input(self.activePlayer[0])
        Y = GPIO.input(self.activePlayer[1])
        Z = GPIO.input(self.activePlayer[2])
    
        #self.setTurn()
        #TODO add WDT
        
        #Loop until proper input is collected
        while True:
            #Initialize Keypad Matrix
            GPIO.output("P8_11", GPIO.HIGH)
        
            if X and not Y and not Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'H'
            elif not X and Y and not Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'S'
            elif X and Y and not Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'D'
            elif not X and not Y and Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'C'
            elif X and not Y and Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'P'
            elif not X and Y and Z:
                GPIO.output("P8_11", GPIO.LOW)
                return 'A'
        
            GPIO.output("P8_11", GPIO.LOW)





       
       
       
       
       
       
