import os
import pandas as  pd
# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
import time #Was using time.sleep(n), but am now using driver.implicitly_wait(n)
# import urllib.request
# import webbrowser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

#Change directory. 
os.chdir("C:/Users/savas/Documents/Ashoka/Economics/IGIDR/Mission Antyodaya/State Dist Block Keys")

df_to_append = list()

###############################################################################

#Obtain master_key - a csv file that has rows of the form: state, district, block. 
master_key = pd.read_csv("state_dist_block_duplicate.csv")

#User Input: Select a state after running the line below. 
master_key.State.unique()

#Copy paste selection from above line here: 
current_state = "RAJASTHAN (8)"

for current_state_loop in master_key.State.unique():
    master_current_state_loop = master_key.loc[(master_key.State == current_state_loop)]
    print("State:", current_state_loop, ", number of GP: ", len(master_current_state_loop))
# # Chooses only our desired state from the main dataframe. 
master_current_state = master_key.loc[(master_key.State == current_state) ]
#Get number of iterations. We can check scraping progress by looking the number of iterations. 
len(master_current_state)



#################

# # IF THE CODE STOPS due to some error:
# # Find the last block the code ran - it does not have to be the last neccesarily, it could be 
# # the second last or third last or fourth last - ie, it doesn't have to be exactly the last. 

# # Enter block below - copy paste it from the python console. 
# stopped_block = "SORAB (5903)"

# # Current state remains the same, so below code is just to reiterate this fact. It does not do anything. 
# master_current_state = master_key.loc[(master_key.State == current_state) ]

# # Index where it stopped:
# index_stopped = master_current_state[master_current_state["Block"] == stopped_block].index[0]
# index_last = master_current_state.ID.iat[-1]

# #Create a list of IDs below the block where our code stopped
# stopped_list = [*range(index_stopped, index_last + 1, 1)]

# #Subset our master key further to only include blocks where the code did not run. Thus, if the code
# #scraped 40 out of 100 observations, the line below subsets the master key such that the code then 
# #runs from observation 40, and not 0. Note that the code can also run from obs 38 and thus have two 
# #duplicates, but we can remove them later easily.
# master_current_state = master_current_state.loc[(master_current_state["ID"].isin(stopped_list))]

#Disable images and get a headless browser. This helps the code run faster.
options = webdriver.ChromeOptions()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

####################

url2 = "https://missionantyodaya.nic.in/preloginStateGPFacilityReports2020.html"

state = current_state  

driver = webdriver.Chrome(options=options, executable_path = "C:/Users/savas/Documents/Ashoka/Economics/IGIDR/Mission Antyodaya/Selenium Driver 2/chromedriver.exe")
driver.implicitly_wait(15)

start_time = time.localtime()
driver.get(url2) #Open URL

#Show all states
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()


state_key = state
driver.find_element_by_link_text(state_key).click() #Find our state and click on it. 

i = 1
for district in master_current_state.District.unique():  
        
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()

    # time.sleep(3)
    
    district_key = district
    driver.find_element_by_link_text(district_key).click()
    
    print("District entered: ", district)

    block_num = 0
    for block in master_current_state.loc[(master_current_state.District == district)].Block:      
  
        block_key = block
        driver.find_element_by_link_text(block_key).click()
        
        #Show all GPs within a block
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()

        # time.sleep(3)  
      
        #Scrape GP table
        dfs = pd.read_html(driver.page_source)[8]
        dfs.columns = ['']*len(dfs.columns)
        dfs["State"] = state
        dfs["District"] = district
        dfs["Block"] = block
        df_to_append.append(dfs)      
          
        #Press back button
        driver.find_element_by_id("backButtion").click()
        # time.sleep(2)
        print ("Scraping over for: " ,state, district, block, i)
        i += 1
        
        block_num += 1
              
        if block_num >= 7 and block_num < 17:
            # driver.find_element_by_id("example_next").click()
            try:
                driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[2]").click()
            except:
                continue
        if block_num >= 17 and block_num < 27:  
            try:
                driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[3]").click()
            except: 
                continue
        if block_num >= 27 and block_num < 37:
            try:
                driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[4]").click()
            except: 
                continue
        if block_num >= 37 and block_num < 47:
            try:
                driver.find_element_by_xpath("//*[@id='example_paginate']/span/a[5]").click()
            except: 
                continue
        if block_num >= 47:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-xs", " " ))]'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']"))).click()

         
    driver.find_element_by_id("backButtion").click()

end_time = time.localtime()       

df_to_append.columns = ['GP', 'government seed centres',
       'warehouse for Food Grain Storage', 'soil testing centres',
       'Fertilizer Shop', 'connected to all weather Road', 'Railway Station',
       'Common Service Centres', 'Panchayat Bhawan',
       'Public Information Board', 'bank', 'ATM', 'Internet/Broadband',
       'Telephone Services', 'Post Office', 'Govt. Degree College', 'Library',
       'Vocational Educational Centres/ITI/RSETI/DDU-GKY',
       'Adult Education Centres', 'Jan Aushadhi kendra', 'PHC/CHC/Sub centers',
       'Public Distribution System(PDS)', 'Aanganwadi Centres',
       'Veterinary Hospital/Clinic', 'Extension facilities for Aquaculture',
       'State', 'District', 'Block']

# df_to_append = df_to_append.drop_duplicates(keep = "first")
df_to_append["ID"] = df_to_append.index

df_to_append.to_csv("Rajasthan_GP.csv")
