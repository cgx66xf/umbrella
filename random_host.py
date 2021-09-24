import random
import socket
import sys
from datetime import datetime


port= 80

def random_ip():	
		random1= random.randint(0, 255)
		random2= random.randint(0, 255)
		random3= random.randint(0, 255)
		random4= random.randint(0, 255)
		randomip= ('{}.{}.{}.{}').format(random1,random2,random3,random4)
		return randomip


def portscan():
	t1 = datetime.now()
	ip= random_ip()
	try:
		socket.setdefaulttimeout(1)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((ip, port))
		if result == 0:
			print("Host up:",ip,port)
		else:
			pass
			#print("Host close:",ip,port,result)
		sock.close()
	except KeyboardInterrupt:
		print ("You pressed Ctrl+C")
		sys.exit()

	except socket.error:
		print ("Couldn't connect to server")
		sys.exit()
	
	t2 = datetime.now()
	#print(t2-t1)
	
while True:
	portscan()	
