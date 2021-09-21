import subprocess
import multiprocessing
import random
import re

def random_ip():	
	random1= random.randint(0, 255)
	random2= random.randint(0, 255)
	random3= random.randint(0, 255)
	random4= random.randint(0, 255)
	randomip= ('{}.{}.{}.{}').format(random1,random2,random3,random4)
	return randomip

def scan_ip():
	masscan= subprocess.run(('timeout 1 ping -c1 {}').format(random_ip()), shell= True, capture_output= True)
	masscan= masscan.stdout.decode()
	return(masscan) 

def grep():
	pattern= re.compile(r'(-{3})(\s)(\d+\.\d+\.\d+\.\d+)')
	matches= pattern.findall(scan_ip())
	for match in matches:
		print(match[2])


while True:
	grep()
	

