from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://washingtondc.craigslist.org/nva")
search = driver.find_element_by_id("query")
search.send_keys("Nikon D7200")
search.send_keys(Keys.ENTER)

driver.find_element_by_name("bundleDuplicates").click()
driver.find_element_by_name("hasPic").click()
driver.find_element_by_name("srchType").click()

minP = driver.find_element_by_name("min_price")
minP.send_keys(500)
#minP.send_keys(Keys.ENTER)
time.sleep(1)
maxP = driver.find_element_by_name("max_price")
maxP.send_keys(800)
maxP.send_keys(Keys.ENTER)