#Complitation1


from time import sleep
import support as spt
import select
import RPi.GPIO as GPIO
import socket

# telemetry values
total_masks = 10
status = "Working"

# operates the dispensors functionality 
def main():
	global total_masks
	global status
	spt.green_led(True)
	spt.red_led(False)
	if (total_masks > 0):		
		if spt.hand_detect():
			spt.set_lcd("Dispensing...   \n                ")
			# initializes servo then opens bottom door
			spt.servo_setup()
			spt.servo_open()

			# spins dispensor stepper motor counter-clock wise
			spt.ccwfine(360)

			# shakes stepper 
			spt.jiggle(4, 20)
			sleep(1)

			# closes bottom door then disconnects servo
			spt.servo_close()
			spt.servo_sleep()

			for i in reversed(range(3)):
				spt.set_lcd("Please Wait: " + str(i) + "\n seconds        " )
				sleep(0.3)
			
			# updates dispensor status
			total_masks -= 1
			status = "Working"
		else:
			spt.set_lcd("hold hand under\n masks left: " +  str(total_masks))
		
		return 1

	else:
		spt.set_lcd("out of masks    \nplease reload :)")
		status = "Empty"
		spt.green_led(False)
		spt.red_led(True)
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

if __name__ == "__main__":
	try:	
		# begins main operations of dispensor
		talk()
		spt.set_lcd("Operation Ended  \n                ")
		sleep(3)
		GPIO.cleanup()

	#exit code with (ctrl) + (c)
	except KeyboardInterrupt:
		spt.p.stop()
		spt.clear_lcd()
		GPIO.cleanup()
		print("program stopped")

GPIO.cleanup()
