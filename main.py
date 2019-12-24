from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import StaleElementReferenceException  
from selenium.common.exceptions import NoSuchElementException 
import json
import ast


browser = webdriver.Chrome(r"D:\webscrapper\drivers\chromedriver.exe")
browser.maximize_window()

page = browser.get('https://www.listennotes.com/podcasts/the-what-bitcoin-did-podcast-peter-mccormack-4n2D3d67Yxk/')
time.sleep(5)

element = browser.find_elements_by_css_selector('.btn.btn-secondary.btn-lg')

while True:
        browser.implicitly_wait(3) 
        try:
            divend = browser.find_elements_by_css_selector(".ln-channel-episodes-pagination-end")
            if(divend):
                  break
        except NoSuchElementException:
                print("Loaded")    
        try:
            element[1].click()
        except StaleElementReferenceException:
            pass 
        time.sleep(3) 
           

episodes_links=[]
for div in  browser.find_elements_by_css_selector('.ln-channel-episode-card-info-title a') :
    episodes_links.append(div.get_attribute('href'))

jsonData =[]
for link in episodes_links:
    data = {}
    episode = requests.get(link)
    time.sleep(3)
    soup = BeautifulSoup(episode.text, 'lxml')
    title = soup.h1.a.text.strip().replace('"', '')
    div = soup.find(class_='ln-channel-episode-description-text')
    pera1 = div.find('p')
    data= {"Url": f"{link}", "Title":f"{title}", "About":list(),"Info":{}, "Connect With": list()}
    startingInfo = ''
   
       
    body = ''
    socialLinkIndex = 0
    i = 0
    for innerPara in  div.find_all('p'):
        if(i != 0):
            if(innerPara.text=='-----'):
                socialLinkIndex =i+1
                break
            elif (innerPara.text.find('Twitter') >= 0 or innerPara.text.find('twitter')>= 0):
                socialLinkIndex =i
                break
            body += innerPara.text.replace('"', '').replace("'", "")
        i+=1
    data['About'].append({
                     f"Body":body     
                        })
    itemInfo = '{'                       
    for initialInfo in pera1.find_all('strong'):
        if(initialInfo.text.find('panel')>=0 or  initialInfo.text.find('Panel')>=0 or initialInfo.nextSibling == None):
            innerInfo='Panel'
            innerInfoValue = initialInfo.text.replace(':','').replace(',','')
        else:
            innerInfo =initialInfo.text.replace(':','').replace(',','')
            innerInfoValue = initialInfo.nextSibling.strip().replace(':','').replace(',','')
        itemInfo+= f'"{innerInfo}":' f'"{innerInfoValue}",'
    
    itemInfoDic = ast.literal_eval(itemInfo.rstrip(',')+'}') 
    data['Info'] =   itemInfoDic           

    ConnectWith = ''
    for innerPara in  div.find_all('p'):
        if(innerPara.text.find('Connect with')>=0 or innerPara.text.find('connect with')>=0):
            for anchor in innerPara.find_all('a'):
                href = anchor['href']
                data['Connect With'].append({
                                    f"{anchor.text}":f"{href}",
                                    })
    jsonData.append(data)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(jsonData, f, ensure_ascii=False, indent=4)