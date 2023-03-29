import os
import pandas as  pd
import math
# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time #Was using time.sleep(n), but am now using driver.implicitly_wait(n)
# import urllib.request
# import webbrowser
from selenium.webdriver.chrome.options import Options
import re

from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

import logging
import pickle

#Add state you want to scrape here with state code in brackets. 
current_state = "TELANGANA (36)"
df_to_append = list()

os.chdir("C:/Users/savas/Documents/Ashoka/Economics/IGIDR/Mission Antyodaya/Python Files/Village_Scraping_To_Send/Data for Village Basic Facilities")
#Get Master CSV file. 
master_current_state = pd.read_csv("Telangana_GP.csv") #change state here. 
master_current_state["ID"] = master_current_state.index
master_current_state = master_current_state[['State', 'District', 'Block', 'GP', 'ID']]


# # IF THE CODE STOPS due to some error:
# #Find the last GP the code ran - it does not have to be the last neccesarily, it could be 
# #the second last or third last or fourth last - ie, it doesn't have to be exactly the last. 

# #Enter GP below - copy paste it from the python console. 
# stopped_gp = "ARASALU (219877)"

# index_stopped =  master_current_state[master_current_state["GP"] == stopped_gp].index[0]
# index_last = master_current_state.ID.iat[-1]

# stopped_list = [*range(index_stopped, index_last + 1, 1)]

# master_current_state = master_current_state.loc[(master_current_state["ID"].isin(stopped_list))] 

options = webdriver.ChromeOptions()
options.headless = True #Dont put headless on for some time. Once code is sorted, then do headless. 
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

url3 = "https://missionantyodaya.nic.in/preloginStateInfrastructureReports2020.html"

def open_url(url3):
    driver.get(url3)
    print("URL Opened")
    return driver

def show_all(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()
    print("Show All Clicked")
    return driver

def scrape(driver, current_state):        
    state = current_state #No point of writing this, but I am writing anyway for good luck. 
    
    state_key = state
    driver.find_element_by_link_text(state_key).click()
    
    i = 1
    for district in master_current_state.District.unique():      
        show_all(driver)
        
        district_key = district    
        driver.find_element_by_link_text(district_key).click()
            
        for block in master_current_state.loc[(master_current_state.District == district)].Block.unique():    
            
            show_all(driver)
      
            block_key = block    
            driver.find_element_by_link_text(block_key).click()
    
            gp_num = 0
            for gp in master_current_state.loc[(master_current_state.Block == block) & 
                                               (master_current_state.District == district)].GP:
                 
              
                gp_key = gp    
                driver.find_element_by_link_text(gp_key).click()
    
                #Get table and concat it to the earlier df
                dfs = pd.read_html(driver.page_source)[8] #Use BS, get id and pass the table. 
                dfs.columns = ['']*len(dfs.columns)
                dfs["State"] = state
                dfs["District"] = district
                dfs["Block"] = block
                dfs["GP"] = gp
                df_to_append.append(dfs) 
                #Remove printing, do logs instead.            
                print("Over: ", state, district, block, gp, i)
                i += 1
                #Press back button and wait for it to load. 
                driver.find_element_by_id("backButtion").click()
                
                gp_num += 1
                  
                if gp_num >= 6 and gp_num < 16:
                    # driver.find_element_by_id("example_next").click()
                    try:
                        driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[2]").click()
                    except:
                        continue
                if gp_num >= 16 and gp_num < 26:
                    try:
                        driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[3]").click()
                    except: 
                        continue
                if gp_num >= 26 and gp_num < 36:
                    try:
                        driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[4]").click()
                    except: 
                        continue
                if gp_num >= 36 and gp_num < 46:
                    try:
                        driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[5]").click()
                    except: 
                        continue
                if gp_num >= 46:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()
    
            #Log every print. 
            # time = time.localtime()
            # print(time.tm_hour,":",time.tm_min, ":", time.tm_sec)
            
            driver.find_element_by_id("backButtion").click()
        
        driver.find_element_by_id("backButtion").click()
        
    return driver
    
if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver = open_url(url3)
    driver = show_all(driver)
    driver = scrape(driver, current_state)
    
    