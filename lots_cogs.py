from selenium import webdriver
import warnings
from google.auth import default
from datetime import date, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
warnings.filterwarnings('ignore')
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("get_gspread_json",scope)
client = gspread.authorize(creds)
driver = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")

def get_data(url):
    sheet = client.open("sheet_name").sheet1 
    driver.get(url)
    try:
        description = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[5]/div[1]/div/div/div[1]/div[2]/div[1]/div').text
    except NoSuchElementException:
        description = ""
    try:
        price = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[5]/div[1]/div/div/div[1]/div[2]/div[2]/div[1]').text
    except NoSuchElementException:
        price = ""
    try:
        mrp = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[5]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]').text
    except NoSuchElementException:
        mrp=""
    try:
        minimum_quantity = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[5]/div[1]/div/div/div[1]/div[2]/div[4]/div/table/tbody/tr/td[1]/div').text
    except:
        minimum_quantity = "None"

    insert=[description,mrp,price,minimum_quantity,url]
    sheet.insert_row(insert,2)
    
if __name__ == '__main__':
    urls = open("lots_url.txt", "r")    
    
    for url in urls.readlines():
        get_data(url)      