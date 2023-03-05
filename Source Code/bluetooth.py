import RPi.GPIO as GPIO

import time
from time import sleep
import serial
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
Buzzer_pin=14
car_pin=21
GPS_pin=18
Button_pin=23
#GPIO.setup(led_pin, GPIO.OUT)

GPIO.setup(GPS_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(car_pin, GPIO.OUT)

GPIO.output(GPS_pin, True)
GPIO.output(car_pin, True)
GPIO.output(led_pin, False)

#LED is connected to Pin 17

GPIO.setup(Button_pin, GPIO.IN) 

#PushButton is connected to Pin 23
#start the configration of Bluetooth conection
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate=9600 ,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
#start Bluetooth conection
ser.isOpen()


try:
    while True:
	    #start with messsage from reciver to get the sensor reading
        user_input = "sensor reading "
		user_input = user_input + '\r'
		#encoding the message 
		ser.write(user_input.encode())
		recv = ''
		tic = time.time()
		while time.time() - tic < 15 and ser.inWaiting() == 0: 
			time.sleep(1)

		if ser.inWaiting() > 0:
			
			recv = ser.read();
		# if the reciver get any reading 
		if recv != '':
            #encode the message 
			recv_encd=  str(recv, 'utf-8')
			sensor_reading=ord(recv_encd)
			print(sensor_reading)
			# check if the reading is normal or not 
			if(sensor_reading<50 or sensor_reading>100 ):

				while True:
                     #when the reading isnot normal and the button is terminated 
					if (GPIO.input (23) == 0 ):        
						print ("Buzzer is OFF")
                       #turn off  buzzer and donot give low signal to the gps and Arm on the car 
						GPIO.output (Buzzer_pin, False)
						GPIO.output(GPS_pin,True)
						GPIO.output(car_pin,True)
					#when the reading isnot normal and the button isnot terminated 	
					if GPIO.input (23) == 1 :

						print ("Buzzer is ON")
                        #give alert up to 30 seconds and then give the signals to start 
						GPIO.output (Buzzer_pin,True)
						sleep(30)
						GPIO.output(GPS_pin,False)
						GPIO.output(car_pin,False)
finally:

    GPIO.cleanup ()
    