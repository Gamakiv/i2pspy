import sqlite3
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import datetime
import timeouts


proxies = {
        'http': 'http://127.0.0.1:4444',
        }

#TODO
#Check open port 4444


def notbon_grabber():
        r = requests.get('http://notbob.i2p/cgi-bin/defcon.cgi', proxies=proxies)
        print('Status requests notbob.i2p: ', r)

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
        chrome_options.add_argument('--disable-in-process-stack-traces')
        chrome_options.add_argument('--output=/dev/null')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome('~/PythonSource/i2pspy/chromedriver', chrome_options=chrome_options)
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


def check_version_record(link):
    sql_connect = sqlite3.connect('db/i2pspy.db')
    cursor = sql_connect.cursor()
    cursor.execute("SELECT MAX(version) FROM spider WHERE link=?", [link])
    version = cursor.fetchone()
    if version[0] == None:
        return 1
    else:
        return version[0]


def data_extraction(site):
        for i in site:
                try:
                    r = requests.get(i, proxies=proxies, timeout=20)
                    now = datetime.datetime.now()

                except:
                    print('Status requests site [', i, ']:  <Response [408M]>')
                    continue

                print('Status requests site [',i, ']: ',r)
                if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        title = soup.find('title')

                        try:
                            stitle = title.get_text()
                            
                        except:
                            stitle = 'Title_None'

                        way_screen = get_screenshot(i) 

                        tmphtml = open('html.tmp', 'w')
                        tmphtml.write(r.text)
                        tmphtml.close()
                        
                        sql_connect = sqlite3.connect('db/i2pspy.db')
                        cursor =sql_connect.cursor()
                        print('Connect SQLite...')

                        if check_version_record(i) != 1:
                            cursor.execute("SELECT hash_html FROM spider WHERE version=?", [check_version_record(i)])
                            hash_in_base = cursor.fetchone()

                            if hash_in_base[0] == get_hash('html.tmp'):
                                print('No changes were detected. Passages...')
                                continue

                            else:
                                print('Changes have been detected. Creating a new version...')
                                db_append = (now.strftime("%d-%m-%Y %H:%M"), 
                                             i, 
                                             stitle, 
                                             r.text, 
                                             get_hash('html.tmp'), 
                                             way_screen, 
                                             check_version_record(i)+1)

                                sql_query = """ INSERT INTO spider 
                                            (dt, link, title, html, hash_html, screenshot, version)
                                            VALUES 
                                            (?, ?, ?, ?, ?, ?, ?);
                                            """

                                cursor.execute(sql_query, db_append)
                                sql_connect.commit()
                                cursor.close()
                                os.remove('html.tmp')

                        else:
                            print('New site when scanning. Adding...')
                            db_append = (now.strftime("%d-%m-%Y %H:%M"), 
                                        i, 
                                        stitle,
                                        r.text, 
                                        get_hash('html.tmp'), 
                                        way_screen, 
                                        1)

                            sql_query = """ INSERT INTO spider 
                                            (dt, link, title, html, hash_html, screenshot, version)
                                            VALUES 
                                            (?, ?, ?, ?, ?, ?, ?);
                                            """

                            cursor.execute(sql_query, db_append)
                            sql_connect.commit()
                            cursor.close()
                            os.remove('html.tmp')

                else:
                        pass
                        ##TODO
                        # add a flag for later checking


data_extraction(notbon_grabber())

