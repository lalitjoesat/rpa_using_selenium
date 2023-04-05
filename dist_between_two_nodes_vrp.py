from selenium import webdriver
import warnings
from google.auth import default
from datetime import date, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#from pprint import pprint as pp
warnings.filterwarnings('ignore')
driver = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")

def get_distance(URL):
    driver.get(URL)
    driver.find_element_by_xpath("//*[@id='hArJGc']/div").click()
    actions = ActionChains(driver)
    x1 = ["28.4317, 77.872", "28.6733, 77.3365", "29.2355, 76.842", "28.7651, 77.7735"]
    x2 = ["29.0457, 77.6588", "28.4247, 77.8599", "28.9793, 77.7588","29.11, 77.0494"]
    driver.implicitly_wait(10)
    for lat in x1:
        for lon in x2:
            start_ = driver.find_element_by_xpath("//*[@id='sb_ifc50']/input")
            start_.clear()
            start_.send_keys(lat)
            end = driver.find_element_by_xpath("//*[@id='sb_ifc51']/input")
            end.clear()
            end.send_keys(lon)

            actions.send_keys(Keys.ENTER)

            actions.perform()

            time_taken = driver.find_element_by_xpath("//*[@id='section-directions-trip-0']/div[1]/div[1]/div[1]/div[1]/span[1]").text
            distance = driver.find_element_by_xpath("//*[@id='section-directions-trip-0']/div[1]/div[1]/div[1]/div[2]/div").text
            
            display(time_taken)
            display(distance)
            break

get_distance("https://www.google.com/maps")
