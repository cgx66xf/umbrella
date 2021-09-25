import random
import socket
import sys 
import threading
import logging
from datetime import datetime

port= 80
target= list()
logging.basicConfig(filename='logs.log', filemode= 'w', level= logging.DEBUG)


def main():

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
				target.append("{}:{}".format(ip, port))
				logging.info("Host {}:{} is up and runtime is {} res:{}".format(ip, port, datetime.now()-t1, result))
			else:
				logging.debug("Host {}:{} is down and runtime is {} res:{}".format(ip, port, datetime.now()-t1, result))
			sock.close()
		except KeyboardInterrupt:
			logging.critical("You pressed Ctrl+C")
			sys.exit()

		except socket.error:
			logging.critical("Couldn't connect to server")
			sys.exit()
	
	threads= []
	while (len(target) < 1):
		for _ in range(5):
			t=threading.Thread(target= portscan)
			t.start()
			threads.append(t)

		for thread in threads:
			thread.join()
		
		if (len(target) == 1):
			return(target[0])
			logging.info(target[0])
		
			
logging.info(print(main()))
