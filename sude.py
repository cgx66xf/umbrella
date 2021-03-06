import requests
import re
import logging
import sqlite3
import ast
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
        self.domain_target= self.find_domain(self.target)
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


def sql_declare():
    global connection
    global cursor
    connection= sqlite3.connect("umbrella.db")
    cursor= connection.cursor()
    cursor.execute("DROP TABLE sude")
    cursor.execute("CREATE TABLE IF NOT EXISTS sude (target TEXT NOT NULL,target_domain TEXT, response_source TEXT, response_headers TEXT, output TEXT)")
    

def scan_save(target): #implement return a boolean value if the target is saved
    scan= Crawler(target, headers)
    target_str= str(scan.target)
    target_domain= str(scan.domain_target)
    source_str= str(scan.response_source)
    headers_str= str(scan.response_headers)
    output_str= str(scan.output)
    cursor.execute("SELECT target FROM sude WHERE target=:scan", {"scan": target_str})
    i= cursor.fetchall()
    if (len(i) == 0):
        cursor.execute("INSERT INTO sude (target, target_domain , response_source, response_headers, output) VALUES (?, ?, ?, ?, ?)",
        (target_str, target_domain, source_str, headers_str, output_str))
        connection.commit()
        logger.info("target not in db:{}".format(target_str))
        return target_domain
    elif (len(i) > 0):
        logger.info("target already in db thus not added: {}".format(target_str))
        return target_domain

def check_number_of_td(target):
    cursor.execute("SELECT target FROM sude WHERE target_domain=:scan", {"scan": target})
    x= cursor.fetchall()
    return len(x)


def main(target, target_length):
    i= 0
    scan= scan_save(target)
    while True:
        i= i+1
        cursor.execute("SELECT output FROM sude WHERE rowid=:i", {"i": i})
        x= cursor.fetchall()
        x= x[0][0]
        x= ast.literal_eval(x)
        print(len(x)) #correct
        for j in range(len(x)):
            scan_save(x[j])
        num= check_number_of_td(scan)
        print("target_length of :{} is: {}".format(target_length, num))
        if (num >= target_length):
            print("target_length reached")
            break

sql_declare()
main('http://python.org/', 0)

connection.close()
