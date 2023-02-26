#import sqlite3
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import datetime


proxies = {
        'http': 'http://127.0.0.1:4444',
        }

#TODO
#Check open port 4444


def notbon_grabber():
        r = requests.get('http://notbob.i2p/cgi-bin/defcon.cgi', proxies=proxies)
        print('Status requests grabber: ', r)

        #TODO
        #if not 200 - repeat

        soup = BeautifulSoup(r.text, 'html.parser')
        b32_list = []

        for link in soup.find_all('a'):
                b32a = link.get('href')
                if b32a.find('b32') > 0 and len(b32a)<69:
                        b32_list.append(b32a)
        return(b32_list)


def get_screenshot(url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1366x768')
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('--proxy-server=127.0.0.1:4444')

        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(3)
        driver.get_screenshot_as_file('screen/tmp.png')
        driver.quit()
        
        new_name = 'screen/' + get_hash('screen/tmp.png') + '.png'
        os.rename('screen/tmp.png', new_name)

        return new_name


def get_hash(filename):
   h = hashlib.sha1()

   with open(filename,'rb') as file:
       chunk = 0

       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()


def data_extraction(site):
        for i in site:
                r = requests.get(i, proxies=proxies)
                now = datetime.datetime.now()

                print('Status requests site [',i, ']: ',r)

                if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        title = soup.find('title')                        
                        print(title.string)
                        way_screen = get_screenshot(i)

                        tmphtml = open('html.tmp', 'w')
                        tmphtml.write(r.text)
                        tmphtml.close()
                        

                        #db_append = (now.strftime("%d-%m-%Y %H:%M"), i, title, r.text, get_hash(memoryfile), way_screen, version)
                else:
                        pass
                        ##TODO
                        # add a flag for later checking


data_extraction(notbon_grabber())

