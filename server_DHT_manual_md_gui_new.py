import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import socket
import picamera	
import picamera.array
import time

host = ''
port = 5591

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)    #Lights
GPIO.setup(22,GPIO.OUT)    #fan
DHT_datapin='4'		   #DHT
sensor=Adafruit_DHT.DHT11

motion_history=[]
threshold = 50    # How Much pixel changes
sensitivity = 250 # How many pixels change


def turnOFF(device):
	GPIO.output(device, GPIO.HIGH)
	pass


def turnON(device):
	GPIO.output(device, GPIO.LOW)
	pass
	
	
def setupServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created.")
	try:
		s.bind((host, port))
	except socket.error as msg:
		print(msg)
	print("Socket bind complete.")
	return s

def setupConnection():
	s.listen(1) # Allows one connection at a time.
	conn, address = s.accept()
	print("Connected to: " + address[0] + ":" + str(address[1]))
	return conn
 
 
def takeMotionImage(width, height):
	with picamera.PiCamera() as camera:
		time.sleep(0.5)
		camera.resolution = (width, height)
		with picamera.array.PiRGBArray(camera) as stream:
			camera.exposure_mode = 'auto'
			camera.awb_mode = 'auto'
			camera.capture(stream, format='rgb')
			return stream.array


def scanMotion(width, height):
	motionFound = False
	data1 = takeMotionImage(width, height)
	time.sleep(0.2)
	data2 = takeMotionImage(width, height)
	diffCount = 0;
	for w in range(0, width):
		for h in range(0, height):
			# get the diff of the pixel. Conversion to int
			# is required to avoid unsigned short overflow.
			diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
			if  diff > threshold:
				diffCount += 1
		if diffCount > sensitivity:
			break;
	if diffCount > sensitivity:
		motionFound = True
	else:
		data2 = data1
	return motionFound

def motionDetection():
	global motion_history
	if scanMotion(224, 160):
		motion_history.append("Motion detected at " + str(time.asctime(time.localtime(time.time()))))


def getDHT():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_datapin)

	while(int(temperature)<20):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_datapin)


	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
	return [temperature,humidity]

def dataTransfer(conn):
	# A big loop that sends/receives data until told not to.
	lights = 0
	fan = 0
	while True:
		try:
			# Receive the data
			data = conn.recv(1024) # receive the data
			data = data.decode('utf-8')
			# Split the data such that you separate the command
			# from the rest of the data.
			dataMessage = data.split(' ', 1)
			command = dataMessage[0]
			motionDetection()
			if command=='TEMP':
				[temperature,humidity]=getDHT()
				reply = "Temperature: " + str(temperature) + " degrees celsius, Humidity: " + str(humidity) + "%"
				# Send the reply back to the client
				#conn.sendall(str.encode(reply))
				print("Data is being transferred!")
			elif command == 'LIGHTS':
				if (lights==0):
					print("Turning on the lights.")
					reply = "Turning on the lights."
					turnON(18)
					lights = 1
				else:
					turnOFF(18)
					print("Turning off the lights.")
					reply = "Turning off the lights."
					lights = 0
			elif command == 'FAN':
				if (fan==0):
					print("Turning on the Fan.")
					reply = "Turning on the Fan."
					turnON(22)
					fan = 1
				else:
					print("Turning off the Fan.")
					turnOFF(22)
					reply = "Turning off the Fan."
					fan = 0
			elif command == 'EXIT':
				print("Our client has left us :(")
				#conn.sendall(str.encode(reply))
				#print("Data has been sent!")
				break
			elif command == 'KILL':
				print("Our server is shutting down.")
				s.close() #Close socket s
				#print("Server shut down")
				#conn.sendall(str.encode(reply))
				#print("Data has been sent!")
				break

			elif command=='MOTION':
				#print("List of Motion History")
				#conn.sendall(str.encode(str(len(motion_history))))
				#print(motion_history)
				for i in motion_history:
					print(i)
					conn.sendall(str.encode(i+"\n"))
				print("Done")
				reply = "List of last motions."
			else:
				reply = 'Unknown Command'
			conn.sendall(str.encode(reply))
			print("Data has been sent!")
			
		except KeyboardInterrupt:
			print("ERROR1")
			s.close()
	conn.close()

s = setupServer()

while True:
	try:
		conn = setupConnection()
		#getDHT()
		dataTransfer(conn)
	except:
		#print(sys.exc_info()[0])
		break
