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
	return matches

def parse_matches():
	for i in nmap():
		if (i[0] == '80'):
			#http_scan()
			print("http0")

		elif (i[0] == '23'):
			#telnet_scan()
			print("telnet0")
		
		elif (i[0] == '443'):
			#https_scan()
			print("https0")

		elif (i[0] == '21'):
			#ftp_scan()
			print("ftp0")

		elif (i[0] == '22'):
			#ssh_scan()
			print("ssh0")

		elif (i[0] == '25'):
			#smtp_scan()
			print("smtp0")
		
		elif (i[0] == '3389'):
			#ms-wbt-server_scan()
			print("ms-wbt-server0")

		elif (i[0] == '110'):
			#pop3()
			print("pop30")

		elif (i[0] == '445'):
			#smb_scan()
			print("smb0")

		elif (i[0] == '139'):
			#netbios-ssn_scan()
			print("netbios-ssn0")

		elif (i[0] == '143'):
			#imap_scan()
			print("imap0")

		elif (i[0] == '53'):
			#dns_scan()
			print("dns0")
		
		elif (i[0] == '135'):
			#msrpc_scan()
			print("msrpc0")

		elif (i[0] == '3306'):
			#mysql_scan()
			print("mysql0")

		elif (i[0] == '8080'):
			#http-proxy_scan()
			print("http-proxy0")

		elif (i[0] == '1723'):
			#pptp_scan()
			print("pptp0")

		elif (i[0] == '111'):
			#rpcbind_scan()
			print("rpcbind0")
		
		else:
			print("unknown port:",i[0])

def http():
	target= "scanme.nmap.org"
	process= subprocess.run('nmap -p80 --script http-auth-finder.nse {}'.format(target), shell= True, capture_output= True)
	result= process.stdout.decode()
	return result

print(http())
