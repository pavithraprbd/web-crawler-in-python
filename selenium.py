#!/usr/bin/python
import subprocess
import json
import os
import re
import sys
from pyvirtualdisplay import Display
from selenium import webdriver
from sh import cd, ls
import time
from tqdm import tqdm
from termcolor import colored
import wget

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import openpyxl as op
from urlparse import urlparse

parent_url = "site url"
login_page ="Login page url"
username_filed_id = "id of the user name filed of the site"
password_filed_id = "id of the password filed of the site"
username = "user name for the logging"
password ="password"
domain = urlparse(parent_url).netloc
# print domain







# crawl_site recusively
def crawl_site(urls_All, urlsCrwld, driver, url):
    
  
    urlsCrwld.append(url)
    
    driver.get(url)
   
    if(url == login_page): #login to the page
    	inputElement = driver.find_element_by_id(username_filed_id)
    	inputElement.send_keys(username)
    	inputElement = driver.find_element_by_id(password_filed_id)
    	inputElement.send_keys(password)
    	inputElement.send_keys(Keys.ENTER)
    html = driver.page_source.encode("utf-8")

    soup = BeautifulSoup(html) #creating tee from html page

    urls = soup.findAll("a")

    
    for a in urls:
        if (a.get("href")) and (a.get("href") not in urls_All):
            urls_All.append(a.get("href"))

    
    for page in set(urls_All):  

       
        print page
        if (urlparse(page).netloc == domain) and (page not in urlsCrwld): # wiill not add to the list if it is alredy there in the list of not in the same domain

        	  # print this_url
        	crawl_site(urls_All, urlsCrwld, driver, page)
           
            

   
    else:
        return urlsCrwld, urls_All






if __name__ == "__main__":
    
    #Maximize the web window
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
  

    urls_All = list()
    urlsCrwld = list()

    urls_All.append(parent_url)

   
    urlsCrwld, urls_All = crawl_site(urls_All, urlsCrwld,
                                        driver, parent_url)

    #quit the browser
    driver.quit()

    print "FULL URLs LIST"
    print len(set(urls_All))

    print "CRAWLED URLs LIST"
    print len(set(urlsCrwld))

  