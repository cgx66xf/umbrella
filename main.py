import sys
import subprocess
import re


def target():
	
	if (len(sys.argv) <= 1):
		print("Invalid amount of arguments, check --help")
	
	elif (len(sys.argv) > 1):
		if (sys.argv[1] == '-u'):
			print("-u flag is selected")
			#task: check if the second argument is valid if so set the target
			target = sys.argv[2]
			return target
			
		elif (sys.argv[1] == '-r'):
			print("-r flag is selected")
			#task: check if path is valid and set the target the path
			
		elif (sys.argv[1] == '-x'):
			print("-x flag is selected")
			import random_host
			target= random_host.main()
			return target
			
		elif (sys.argv[1] == '--help'):
			print("--help flag is selected")
		
		else:
			print("arguments are weird, check --help")

def nmap():  #this returns the open ports against a target
	enemy= "scanme.nmap.org"
	process= subprocess.run('nmap {}'.format(enemy), shell= True, capture_output= True)
	result= (process.stdout.decode())
	pattern= re.compile(r'(\d+)\/(tcp|udp)\s+(open|filtered)\s+(\S+)')
	matches= pattern.findall(result)
	return (matches)
	
nmap()

	
		
