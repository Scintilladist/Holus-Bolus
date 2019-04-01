import socket
import sys
from time import sleep

from tkinter import *
#import next_screen.py

host = '192.168.43.119'
port = 5591

def command1(command):
	if(command=='EXIT'):
		#Send exit request to other end
		s.send(str.encode(command))
		gui.quit()
		#break
	elif(command=='KILL'):
		#s.send(str.encode(command))
		#sleep(2)
		s.close()
		#reply=s.recv(1024)
		gui.destroy()
	elif(command=='MOTION'):
		s.send(str.encode(command))
		reply=s.recv(1024)
		print(reply.decode('utf-8'))
		print("\n")
		reply=s.recv(1024)
		print(reply.decode('utf-8'))
		#reply=s.recv(1024)
		#print("Number of motion detects: ", reply.decode('utf-8'))
		#for i in range(int(reply.decode('utf-8'))):
			#reply1=s.recv(1024)
			#print(reply1.decode('utf-8'))
		#reply=s.recv(1024)
		#print(reply1.decode('utf-8'))
	elif(command=='TEMP'):
		s.send(str.encode(command))
		reply=s.recv(1024)
		print(reply.decode('utf-8'))
	elif(command=='LIGHTS'):
		s.send(str.encode(command))
		reply=s.recv(1024)
		print(reply.decode('utf-8'))
	elif(command=='FAN'):
		s.send(str.encode(command))
		reply=s.recv(1024)
		print(reply.decode('utf-8'))

'''	
def clear(): 
    s.close()
'''    
def create_window():
    testtk = Toplevel(next_screen.py)


def setupSocket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s






###############################################################################

s = setupSocket()


# create a GUI window 
gui = Tk() 

# set the background colour of GUI window 
gui.configure(background="white") 

# set the title of GUI window 
gui.title("Magic Box") 

# set the configuration of GUI window 
gui.geometry("365x225") 

# StringVar() is the variable class 
# we create an instance of this class 
equation = StringVar() 

# create the text entry box for 
# showing the expression . 
expression_field = Entry(gui, textvariable=equation) 

# grid method is used for placing 
# the widgets at respective positions 
# in table like structure . 

# create a Buttons and place at a particular 
# location inside the root window . 
# when user press the button, the command or 
# function affiliated to that button is executed . 
button1 = Button(gui, text=' DHT Values ', fg='black', bg='grey', 
				 command=lambda: command1("TEMP"), height=2, width=10) 
button1.grid(row=2, column=0) 

button2 = Button(gui, text=' Motion Detection ', fg='black', bg='grey', 
				 command=lambda: command1("MOTION"), height=2, width=13) 
button2.grid(row=2, column=1) 


button3 = Button(gui, text='Lights', fg='black', bg='grey', 
				 command=lambda: command1("LIGHTS"), height=2, width=10) 
button3.grid(row=5, column=0)


button4 = Button(gui, text='Fan', fg='black', bg='grey', 
				 command=lambda: command1("FAN"), height=2, width=13) 
button4.grid(row=5, column=1)

button5 = Button(gui, text='Close connection', fg='black', bg='grey', 
				 command=lambda: command1("KILL"), height=2, width=13) 
button5.grid(row=8, column=1)

clear = Button(gui, text='Clear', fg='black', bg='grey', 
			   command=lambda: command1("EXIT"), height=2, width=10) 
clear.grid(row=8, column=0) 

# start the GUI 
gui.mainloop() 


s.close()
