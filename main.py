import sys
import subprocess
import re
import logging


def create_logger():
    # create logger for "Sample App"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('results.log', mode='w')
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s' +
                                  '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

logger = create_logger()


def target():
	
	if (len(sys.argv) <= 1):
		logger.warning(print("Invalid amount of arguments, check --help"))
	
	elif (len(sys.argv) > 1):
		if (sys.argv[1] == '-u'):
			print("-u flag is selected")
			logger.debug("-u flag is selected")
			#task: check if the second argument is valid if so set the target
			target = sys.argv[2]
			return target
			
		elif (sys.argv[1] == '-r'):
			print("-r flag is selected")
			logger.debug("-r flag is selected")
			#task: check if path is valid and set the target the path
			
		elif (sys.argv[1] == '-x'):
			print("-x flag is selected")
			logging.debug("-x flag is selected")
			try:
				import random_host
			except ImportError:
				logger.warning("ImportError")
			else:
				logger.debug("random_host imported successfully")
			target= random_host.main()
			return target
			
		elif (sys.argv[1] == '--help'):
			print("--help flag is selected")
		
		else:
			print("arguments are weird, check --help")


def nmap():  #this returns the open ports against a target
	enemy= target()
	process= subprocess.run('nmap {}'.format(enemy), shell= True, capture_output= True)
	result= (process.stdout.decode())
	pattern= re.compile(r'(\d+)\/(tcp|udp)\s+(open|filtered)\s+(\S+)')
	matches= pattern.findall(result)
	return matches

def parse_matches():
	for i in nmap():
		if (i[0] == '80'):
			print("http0")
			p1= Http_brute()
			p1.http_auth_finder()
			p1.parse_http_auth_finder()

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

class Http_brute():
	def http_auth_finder(self):
		self.target= "192.168.1.1"
		self.process= subprocess.run('nmap -p80 --script http-auth-finder.nse {}'.format(self.target), shell= True, capture_output= True)#i[0]= prepath i[1]=/path i[2]=FORM or HTTP
		self.result= self.process.stdout.decode()
		self.pattern= re.compile(r'(https?:\/\/[^/]+)(\S*)\s+(FORM|HTTP)')
		self.matches= self.pattern.findall(self.result)
		return self.matches

	def http_brute(self, auth_path):
		print("bruting auth at:",auth_path)
		self.process= subprocess.run('nmap --script http-brute.nse {} [--script-args http-brute.path={}] -p80'.format(self.target, auth_path), shell= True, capture_output= True)
		self.result= self.process.stdout.decode()
		print(self.result)

	def http_form_brute(self, form_path):
		print("bruting form at:",form_path)
		self.process= subprocess.run('nmap --script http-form-brute.nse {} [--script-args http-form-brute.path={}] -p80 '.format(self.target, form_path), shell= True, capture_output= True)
		self.result= self.process.stdout.decode()
		print(self.result)

	
	def parse_http_auth_finder(self):
		if (len(self.matches) > 0):
			for i in self.matches:
				if (i[2] == 'HTTP'):
					print("HTTP auth detected")
					self.http_brute(i[1])

				elif (i[2] == 'FORM'):
					print("FORM auth detected ")
					self.http_form_brute(i[1])
					
			    
				else:
					print("parse_http_auth_finder: Type not detected")			    

parse_matches()
