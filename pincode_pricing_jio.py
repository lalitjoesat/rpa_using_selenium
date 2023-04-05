from selenium import webdriver
import warnings
from google.auth import default
from datetime import date, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
#from pprint import pprint as pp
warnings.filterwarnings('ignore')
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("get_gspread_key",scope)
client = gspread.authorize(creds)
driver = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
def main(pin_code):
    sheet = client.open("sheet_name").sheet1 
    sampl = date.today()
    today = str(sampl)
    jio_urls = open("jiourls.txt", "r")
    for jio_url in jio_urls.readlines():
        driver.get(jio_url)
        driver.implicitly_wait(20)
        try:
            driver.find_element_by_id("btn_delivery").click()
            driver.implicitly_wait(10)
            driver.find_element_by_id("btn_enter_pincode").click()
            username1 = driver.find_element_by_id("rel_pincode")
            driver.implicitly_wait(5)
            username1.send_keys(pin_code)
        except NoSuchElementException: 
            print("No")
        print(driver.find_element_by_id("is_in_stock").text)
        if driver.find_element_by_id("is_in_stock").text=="Unavailable at your location":
            try:
                title_name = driver.find_element_by_xpath("//*[@id='pdp_product_name']").text
            except NoSuchElementException:
                title_name = "NA"
            pass
            
        else:
            try:
                title = driver.find_element_by_xpath("//*[@id='pdp_product_name']")
                title_name=title.text
                    
            except NoSuchElementException:
                title_name = "NA"
            try:
                get_mrp = driver.find_element_by_xpath('/html/body/main/section/section[2]/div[1]/div/div[2]/div/section[2]/div[1]/div[1]/div[2]/span[1]').text
                extract_number = re.split("₹",get_mrp)
                remove_comma = extract_number[1]
                new_mrp = remove_comma.replace(",",'')
                mrp = float(new_mrp)
                
            except NoSuchElementException:
                mrp = ""
            try:
                get_sp = driver.find_element_by_xpath('/html/body/main/section/section[2]/div[1]/div/div[2]/div/section[2]/div[1]/div[1]/div[1]/span[1]').text
                extract_number_from_sp = re.split("₹",get_sp)
                remove_comma_from_sp = extract_number_from_sp[1]
                new_sp = remove_comma_from_sp.replace(",",'')
                sp = float(new_sp)
            
            except NoSuchElementException:
                sp = ""
            pin_code1=int(pin_code)
            insert=[title_name,mrp,sp,pin_code1,today,jio_url,"","","",""]
            sheet.insert_row(insert,2)
        
if __name__ == '__main__':
    pin_codes = open("pin.txt", "r")    
    
    for pin_code in pin_codes.readlines():
        main(pin_code)