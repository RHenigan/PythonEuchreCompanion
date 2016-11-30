import Adafruit_BBIO.GPIO as GPIO

#TODO avoid using predesignated pins
GPIO.setup("P8_11", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #Clock
GPIO.setup("P8_12", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P1 X
GPIO.setup("P8_13", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_14", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_15", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P2 X
GPIO.setup("P8_16", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_17", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_18", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P3 X
GPIO.setup("P8_19", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_27", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_28", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #P4 X
GPIO.setup("P8_29", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Y
GPIO.setup("P8_30", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Z
GPIO.setup("P8_39", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P1 Turn
GPIO.setup("P8_40", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P2 Turn
GPIO.setup("P9_23", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P3 Turn
GPIO.setup("P9_25", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P4 Turn
GPIO.setup("P9_27", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P1 Deal
GPIO.setup("P9_28", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P2 Deal
GPIO.setup("P9_29", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P3 Deal
GPIO.setup("P9_30", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                             #P4 Deal
GPIO.setup("P9_31", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	if GPIO.input("P8_11"):
		print("11")
	elif GPIO.input("P8_12"):
		print("12")	
	elif GPIO.input("P8_13"):
		print("13")
	elif GPIO.input("P8_14"):
		print("14")
	elif GPIO.input("P8_15"):
		print("15")
	elif GPIO.input("P8_16"):
		print("16")
	elif GPIO.input("P8_17"):
		print("17")
	elif GPIO.input("P8_18"):
		print("18")
	elif GPIO.input("P8_19"):
		print("19")
	elif GPIO.input("P8_27"):
		print("27")
	elif GPIO.input("P8_28"):
		print("28")
	elif GPIO.input("P8_29"):
		print("29")
	elif GPIO.input("P8_30"):
		print("30")
	elif GPIO.input("P8_39"):
		print("39")
	elif GPIO.input("P8_40"):
		print("40")
	elif GPIO.input("P9_23"):
		print("23")
	elif GPIO.input("P9_25"):
		print("25")
	elif GPIO.input("P9_27"):
		print("27")
	elif GPIO.input("P9_28"):
		print("28")
	elif GPIO.input("P9_29"):
		print("29")
	elif GPIO.input("P9_30"):
		print("30")
	elif GPIO.input("P9_31"):
		print("31")
