import random
import socket
import sys 
import threading
from datetime import datetime

port= 80
target= list()

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
				#print("Host {}:{} is up and runtime is {} res:{}".format(ip, port, datetime.now()-t1, result))
			else:
				pass
				#print("Host {}:{} is down and runtime is {} res:{}".format(ip, port, datetime.now()-t1, result))
			sock.close()
		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.error:
			print ("Couldn't connect to server")
			sys.exit()
	
	threads= []
	while (len(target) < 1):
		for _ in range(10):
			t=threading.Thread(target= portscan)
			t.start()
			threads.append(t)

		for thread in threads:
			thread.join()
		
		if (len(target) == 1):
			return(target[0])
		
			
main()
