#Complitation1

#---------------------libraries-----------------------------------

#stepper
import threading
from time import sleep
import RPi.GPIO as GPIO

#lcd
import board
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

#servo
from gpiozero import Servo

#communication socket
import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(10)

#---------------------constants------------------------------------
total_masks = 12
status = "Working"

#stepper pins
IN1=12 # IN1
IN2=16 # IN2
IN3=20 # IN3
IN4=21 # IN4

# Time betwwen stepper steps
time = 0.001

#stepper motor rotation calibration 
#(=desired/actual) most recent: 10 r code: 7.05 actual
mrc = 1.4184

#LCD constants
lcd_columns = 16
lcd_rows = 2

#lcd pins declared in init

#button Pin
Button_pin = 17

#servo pin
servo = 23

#servo duty cycle range
lower_dc = 1 #-90 deg
upper_dc = 13   #90 deg

#ir pins
ir_en = 24 #enable
ir_out = 25 #output

#---------------------initialising---------------------------------
# set board reference mode
GPIO.setmode(GPIO.BCM)

#stepper pins
# set pins as outputs
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

#Set output pins to low.
GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)

#set up lcd pins as outputs
lcd_rs = DigitalInOut(board.D22)
lcd_en = DigitalInOut(board.D5)
lcd_d4 = DigitalInOut(board.D6)
lcd_d5 = DigitalInOut(board.D13)
lcd_d6 = DigitalInOut(board.D19)
lcd_d7 = DigitalInOut(board.D26)

# Initialise the LCD class
lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Clear LCD
lcd.message = " clear \n clear"
sleep(3)

#set button pin to low input
GPIO.setup(Button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Set servo control pi as output
GPIO.setup(servo, GPIO.OUT)

#initialize pwm for servo pin
p = GPIO.PWM(servo, 50) # second argument is hertz, sg90 servo runs on 50Hz logic

#Set servo initial position to 0 deg = 7ms duty cycle
p.start(2)

#ir setup
GPIO.setup(ir_en,GPIO.OUT)
GPIO.setup(ir_out,GPIO.IN)

#cheeky delay for safety
sleep(1)

#----------------------Stepper Method-----------------------------

def Step1():
    #0001
    stepCode = [0, 0, 0, 1]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step2():
    #0011
    stepCode = [0, 0, 1, 1]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step3():
    #0010
    stepCode = [0, 0, 1, 0]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step4():
    #0110
    stepCode = [0, 1, 1, 0]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step5():
    #0100
    stepCode = [0, 1, 0, 0]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)
 

def Step6():
    #1100
    stepCode = [1, 1, 0, 0]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step7():
    #1000
    stepCode = [1, 0, 0, 0]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


def Step8():
    #1001
    stepCode = [1, 0, 0, 1]
    GPIO.output(IN1, stepCode[0])
    GPIO.output(IN2, stepCode[1])
    GPIO.output(IN3, stepCode[2])
    GPIO.output(IN4, stepCode[3])
    sleep(time)


# Umdrehung links herum  
def ccwfine(step):	
	for i in range (int(round(step*mrc))):   
		Step1()
		Step2()
		Step3()
		Step4()
		Step5()
		Step6()
		Step7()
		Step8()  
		print( "Step Counter Clockwise: ",i)

def ccwcoarse(step):	
	for i in range (int(round(step*mrc))):   
		Step1()
		Step3()
		Step5()
		Step7()
		print( "Step Counter Clockwise: ",i)
		
def ccwfulltorque(step):	
	for i in range (int(round(step*mrc))):   
		Step4()
		Step6()
		Step8()
		Step2()
		print( "Step Counter Clockwise",i)

# Umdrehung rechts herum		
def cwfine(step):
	for i in range (int(round(step*mrc))):
		Step8()
		Step7()
		Step6()
		Step5()
		Step4()
		Step3()
		Step2()
		Step1()  
		print( "Step Clockwise",i)
        
def cwcoarse(step):
	for i in range (int(round(step*mrc))):
		Step7()
		Step5()
		Step3()
		Step1()  
		print( "Step Clockwise",i)
        
def cwfulltorque(step):	
	for i in range (int(round(step*mrc))):   
		Step2()
		Step8()
		Step6()
		Step4()
		print( "Step Clockwise",i)


#----------------------LCD Methods --------------------------------
def set_lcd(message):
	lcd.message = str(message)
	#
	
def clear_lcd():
	lcd.message = "                \n                "
	
#-----------------------Button Methods----------------------------

def button_pressed():
	if(GPIO.input(Button_pin)):   
		#print('y')
		return True
	else:     
		#print('n')
		return False
	time.sleep(0.1)
#-------------------------Servo Methods ---------------------------

def servo_full_sweep():
	#run each step from 5 - 10
	j = 8
	for i in range((lower_dc*j),((upper_dc+1)*j)):
		p.ChangeDutyCycle((i/j)) #argument is the %duty cycle = duty/frequency, 1/20ms = 5% == -90
		sleep(0.1/j)
        
	#run each step from 9 to 6 | net: 5,6,7,8,9,10,,9,8,7,6,
	for i in reversed(range(((lower_dc+1)*j),(j*upper_dc))):
		p.ChangeDutyCycle((i/j)) #argument is the %duty cycle = duty/frequency, 1/20ms = 5% == -90
		sleep(0.1/j) 

#-----------------ir methods-------------------------------------------
def ir_check():
	GPIO.output(ir_en, True)
	sleep(0.001)
	x = GPIO.input(ir_out)
	GPIO.output(ir_en, False)
	return x
    
def hand_detect():
	x = False
	if not ir_check():
		if not ir_check():
			if not ir_check():
				if not ir_check():
					x = True
	return x

#-----------------Main-------------------------------------------

def main():
	global total_masks
	global status
	total_masks = 12
	while (total_masks>0):
		if hand_detect():
			set_lcd("360 Stepper     \n                ")
			
			for i in reversed(range(5)):
				print("rotating stepper in: ", i)
				sleep(0.1)
				
			ccwfine(360)
			
			set_lcd("180 Servo       \n                ")
			for i in reversed(range(5)):
				print("sweeping servo in: ", i)
				sleep(0.1)
				
			servo_full_sweep()
			
			for i in reversed(range(5)):
				print("program exiting in: ", i)
				sleep(0.1)
			
			total_masks -= 1
			status = "Working"
		else:
			set_lcd("push to run     \n masks left: " +  str(total_masks))
			status = "No Masks"

		
	set_lcd("out of masks    \nplease reload :)")
	sleep(3)

def talk():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((socket.gethostname(), 1234))
	s.listen(5)
	while True:
		clientsocket,address = s.accept()
		msg = str(str(total_masks) + ":" + status)
		clientsocket.send(bytes(msg,"utf-8"))		
		

try:	
	thr1 = threading.Thread(target=main)
	thr1.start

	thr2 = threading.Thread(target=talk)
	thr2.start

	thr1.join
	thr2.join

	set_lcd("     cleanup    \n                ")
	sleep(3)
	GPIO.cleanup()

#exit code with (ctrl) + (c)
except KeyboardInterrupt:
	p.stop()
	clear_lcd()
	GPIO.cleanup()
	print("program stopped")

GPIO.cleanup()