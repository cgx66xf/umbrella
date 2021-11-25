import socket
import logging
import datetime
import sys

def main(target):
    socket.setdefaulttimeout(1)
    for i in range(500):
        try:
            sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, i))

        except KeyboardInterrupt:
            print("ctrl+c")
            sys.exit()

        except socket.error:
            print("socket error")
            sys.exit()
        
        print("port: {} result: {}".format(i, result))

main(http://scanme.nmap.org/)
    