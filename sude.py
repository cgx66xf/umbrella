from os import terminal_size
import requests
import re
import logging
from urllib.parse import urljoin
from urllib.parse import urlparse

headers= { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    }


class Crawler():
    def __init__(self, target, headers):
        self.target= target
        #logger.debug(self.target)
        self.headers= headers
        #logger.debug(self.headers)
        self.get_source()
        self.collect_links()
        self.parse_external()
        self.urljoin_internal()
        self.remove_duplicates()

    def get_source(self):
        self.response= requests.get(self.target)
        self.response_source= self.response.text
        #logger.debug("Response source:", self.response_source)
        self.response_headers= self.response.headers
        #logger.debug(self.response_headers)

    def collect_links(self):
        pattern= re.compile(r'<a\shref="([^"]+)"')
        self.matches= pattern.findall(self.response_source)
        logger.debug(self.matches)
        self.external= list()
        self.internal= list()
        for match in self.matches:
            if (urlparse(match).scheme == 'https'):
                self.external.append(match)
                logger.debug("external:"+ match)
            elif (urlparse(match).scheme == 'http'):
                self.external.append(match)
                logger.debug("external:"+ match)
            else:
                self.internal.append(match)
                logger.debug("internal:"+ match)

    def find_domain(self, target): #when you input a url it outputs the domain
        target= urlparse(target).netloc
        j= -1
        pos1= ''
        pos2= ''
        for i in target:
            j+= 1
            if (i == '.'):
                if (len(str(pos1)) > 0 and len(str(pos2)) > 0):
                    break

                elif (len(str(pos1)) > 0):
                    pos2= j
                    #logger.debug("pos2:"+ str(pos2))
                
                elif (len(str(pos1)) == 0):
                    pos1= j
                    #logger.debug("pos1"+ str(pos1))

        #no subdomain and domain is netloc
        if (len(str(pos1)) > 0 and len(str(pos2)) == 0):
            return target
        #indexes before the first (dot) is subdomain and indexes after the first dot in the netloc is the domain
        elif (len(str(pos1)) > 0 and len(str(pos2)) > 0):
            return (target[pos1+1:])

        elif (len(str(pos1)) == 0 and len(str(pos2)) > 0):
            print("ERROR")
            logger.warning("ERROR")

        elif (len(str(pos1)) == 0 and len(str(pos2)) == 0):
            print("ERROR")
            logger.warning("ERROR")
        

    def parse_external(self):
        self.output2= list()
        self.domain_target= self.find_domain(self.target)
        logger.info("external before remove:{}".format(self.external))
        removed_num= 0
        for i in self.external:
            if (self.find_domain(i) == self.domain_target):
                logger.debug("{} == {}".format(i, self.domain_target))
                self.output2.append(i)

            elif (self.find_domain(i) != self.domain_target):
                logger.debug("{} != {} and removed".format(i, self.domain_target))
                self.external.remove(i)
                removed_num += 1

            else:
                logger.debug("WEIRD STATE!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.info("external after remove:{}".format(self.external))
        logger.info("removed item count:{}".format(removed_num))
        
    def urljoin_internal(self):
        if (len(self.internal) > 0):
            for i in self.internal:
                i= urljoin(self.target, i)
                self.output2.append(i)

    def remove_duplicates(self):
        self.output= list()
        for i in self.output2:
            if i not in self.output:
                self.output.append(i)

def create_logger():
    # create logger for "Sample App"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('logs.log', mode='w')
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s' +
                                  '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
logger= create_logger()

def main(target, scan_length):
    scan= Crawler(target, headers)
    scan_all= [[scan.target, scan.response_source, scan.response_headers, scan.output]]
    for i in scan_all[0][3]:
        print(i)
        if i not in scan_all[0]:
            scan= Crawler(i, headers)
            scan_all.append([scan.target, scan.response_source, scan.response_headers, scan.output])
    for j in range(len(scan_all)):
        print(scan_all[j][0])
        print("*"*100)
    

main('http://python.org/',0)
