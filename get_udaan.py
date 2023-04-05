from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
import warnings
from datetime import date, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time
import datetime
from selenium.webdriver.common.keys import Keys
import pandas as pd
import regex as re
import sqlalchemy 
import gspread
from google.auth import default

from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("get_gspread_json_key",scope)
client = gspread.authorize(creds)


warnings.filterwarnings('ignore')


def create_driver():
    opt = Options()
    opt.add_experimental_option("debuggerAddress","localhost:8989")
    driver = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe", chrome_options=opt)
    return driver
    
def get_attributes(link):
    sheet = client.open("jio_prices").sheet1 
    date_ = date.today() 
    data_to_dict = {'product_name':[],
                    'price':[],
                    'details' : [],
                    'min_quantity':[],
                    'price_updated_on' : []}
    driver=create_driver()
    driver.get(link)
    driver.implicitly_wait(5)
    try:                    
        driver.find_element(By.XPATH,"//*[@id='appFlavourSelector_food_and_fmcg']/div/div[2]/div[1]/div[2]/div").click()
    except NoSuchElementException:
        pass
            
    #time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 10);")
    
    time.sleep(10)
    #driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    c=1
    for i in range(5):
        c+=1
        try:  
            name= driver.find_element(By.XPATH,f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[1]/div[1]/div").text
        except:
            name = "NA"
        try:
            price = driver.find_element(By.XPATH,f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div[4]/div[2]/div[1]").text
        except:
            price="NA"
            if price=="NA":
                try: 
                    price=driver.find_element(By.XPATH,f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div[3]/div[2]/div[1]").text
                except:
                    price="NA"
                    if price=="NA":
                        try:
                            price=driver.find_element(By.XPATH,f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]").text
                        except:
                            price=="NA"
                            if price=="NA":
                                try:
                                    price=driver.find_element(By.XPATH,f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div/div/div/div[1]/div/div[1]").text
                                except:
                                    price="NA"
                                    
        try:
            details = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[2]/div").text
        except:
            details="NA"
            
        try:
            min_quantity = driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div[4]/div[1]/div").text
        except:
            min_quantity = "NA"
            if min_quantity == "NA":
                try:
                    min_quantity=driver.find_element(By.XPATH, f"//*[@id='root']/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[{c}]/div[1]/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div").text
                except:
                    min_quantity="NA"
                    if min_quantity=="NA" and name == "NA" and details == "NA":
                        min_quantity = "NA"
                    else:
                        min_quantity="1pc"

        
        if "MRP" in details:
            for j in details:
                if j=="M":
                    y=details.index("M")
                    mrp_ = details[y:y+9]
                    if "|" in mrp_:
                        get_mrp = re.split(" ", details)
                        count_again = 0
                        for j in get_mrp:
                            if count_again == 1:
                                mrp=j
                                break
                            else:
                                count_again+=1
        else:
            mrp=""

        into_list = [name,mrp,price,details,min_quantity]
        sheet.insert_row(into_list,2)
    

if __name__ == "__main__":
    links = open("C:/Users/lalit/udaan_links.txt", "r")
    
    for link in links:
        get_attributes(link)
        