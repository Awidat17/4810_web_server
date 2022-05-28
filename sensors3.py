#Complitation1

#---------------------libraries-----------------------------------

#stepper
import support as spt
import select
from time import sleep
import RPi.GPIO as GPIO

#communication socket
import socket

#---------------------constants------------------------------------

# status to be reported
total_masks = 10
status = "Working"

#-----------------Main-------------------------------------------

# operates the dispensors functionality 
def main():
	global total_masks
	global status
	if (total_masks>0):
		if spt.hand_detect():
			spt.set_lcd("360 Stepper     \n                ")
			for i in reversed(range(5)):
				print("rotating stepper in: ", i)
				sleep(0.1)
			
			spt.servo_open()
			spt.ccwfine(360)
			
			spt.set_lcd("180 Servo       \n                ")
			
			for i in reversed(range(5)):
				print("sweeping servo in: ", i)
				sleep(0.1)
				
			spt.servo_close()
			
			for i in reversed(range(3)):
				spt.set_lcd("Please Wait: " + str(i) + "\n seconds        " )
				print("program exiting in: ", i)
				sleep(0.3)
				
			total_masks -= 1
			status = "Working"
		else:
			spt.set_lcd("push to run     \n masks left: " +  str(total_masks))
		
		return 1
	else:
		spt.set_lcd("out of masks    \nplease reload :)")
		status = "Empty"
		return 0	

# handles communication and main dispenser operations
def talk():
	# creates socket for communication with webserver
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((socket.gethostname(), 4321))
	s.listen(10)

	# creates polling object
	pollObject = select.poll()
	pollObject.register(s, select.POLLIN)

	while True:
		# polls socket for 10ms then sends status information to webserver clients
		pollData = pollObject.poll(10)
		for fd, event in pollData:
			clientsocket,address = s.accept()
			msg = str(str(total_masks) + ":" + status)
			clientsocket.send(bytes(msg,"utf-8"))
			clientsocket.close()

		# main() returns 1 if there are still masks and 0 if none are left or error occurs
		if not main():
			# send final status information
			pollData = pollObject.poll(10)
			for fd, event in pollData:
				clientsocket,address = s.accept()
				msg = str(str(total_masks) + ":" + status)
				clientsocket.send(bytes(msg,"utf-8"))
				clientsocket.close()
			s.close()
			sleep(3)
			break


try:	
	talk()
	spt.set_lcd("     cleanup    \n                ")
	sleep(3)
	GPIO.cleanup()

#exit code with (ctrl) + (c)
except KeyboardInterrupt:
	spt.p.stop()
	spt.clear_lcd()
	GPIO.cleanup()
	print("program stopped")

GPIO.cleanup()