from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from more_itertools import unique_everseen
from pprint import pprint
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from collections import OrderedDict
from datetime import date
import time
import csv


driver = webdriver.Chrome()
driver.get("https://washingtondc.craigslist.org/nva")
search = driver.find_element_by_id("query")

#Inputing the search keyword
search.send_keys("Canon")
search.send_keys(Keys.ENTER)

#Selecting the photo/video and electronics cateories
driver.find_element_by_css_selector('input.catcheck.selectallcb').click()
driver.find_element_by_css_selector(".catcheck.multi_checkbox[id='cat_pha']").click()
driver.find_element_by_css_selector(".catcheck.multi_checkbox[id='cat_ela']").click()
driver.find_element_by_css_selector("button.searchlink.linklike.changed_input.clickme").click()
#Bundling duplicates, requiring pictures, not including nearby searches
driver.find_element_by_name("bundleDuplicates").click()
driver.find_element_by_name("hasPic").click()
driver.find_element_by_name("searchNearby").click()

#Inputing the min and max price
minP = driver.find_element_by_name("min_price")
minP.send_keys(500)
time.sleep(1)
maxP = driver.find_element_by_name("max_price")
maxP.send_keys(900)
maxP.send_keys(Keys.ENTER)

#Prepping for beautiful soup
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

#Going through all content divs and finding the links
nduplinks = []
duplinks=[] 
#Finding the non duplicated results
nonDups = soup.findAll('li', {'class': 'result-row'})
for item in nonDups:
    nduplinks.append(item.find('a').get('href'))
#Finding the duplicated results
dups = soup.findAll('ul', {'class': 'duplicate-rows'})
for item in dups:
    duplinks.append(item.find('a').get('href'))

#Removing the duplicates, returning the links list
links = [x for x in nduplinks if x not in duplinks]

#Removing duplicate links due to pictures and titles both being the same
links = list(unique_everseen(links))
while "#" in links:
    links.remove("#")

#Clicking into the item links
count = 0
dailyitems=[]
itemDict = []
for link in links:
    #Clicking the item link
    link = '"'+link+'"'
    print(link)
    element = driver.find_element_by_xpath('//a[@href=%s]' %link)
    driver.execute_script('arguments[0].click();', element)

    #Getting the item html for beautiful soup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #Getting the item price and title
    price = soup.find('span', {'class': 'price'}).get_text()
    title = soup.find('span', {'id': 'titletextonly'}).get_text()
    #Getting the item text
    text = soup.find('section', {'id':'postingbody'}).get_text()
    while "\n" in text:
        text = text.replace("\n", "")
    while "QR Code Link to This Post" in text:
        text = text.replace("QR Code Link to This Post", "")
    itemD = {"Title":title, "Price":price, "Description":text}

    #Making a list of dictionaries
    itemDict.append(itemD)

    #Adding to a list
    dailyitems.append([itemD['Title'], itemD['Price'], itemD['Description']])
    count += 1
    driver.back()

#Outputting the results array item by item
pprint(dailyitems)
df = pd.DataFrame(itemDict)
#print(df)

#Joining descriptions for a wordcloud
s = ''
for item in dailyitems:
    s += item[2]
# print(s)
# wordcloud = WordCloud().generate(s)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

#Making an image in the shape of the camera
# read the mask image
col = Image.open("/Users/mikes/Documents/GetawayDevelopment/camera.jpg")
gray = col.convert('L')
bw = gray.point(lambda x: 0 if x<230 else 255, '1')
bw.save("/Users/mikes/Documents/GetawayDevelopment/camera_mask.jpg")

camera_mask = np.array(Image.open("/Users/mikes/Documents/GetawayDevelopment/camera_mask.jpg"))

wc = WordCloud(background_color="white", max_words=2000, mask=camera_mask)
# generate word cloud
wc.generate(s)

# store to file
wc.to_file("/Users/mikes/Documents/GetawayDevelopment/canon.jpg")

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(camera_mask, cmap='gray', interpolation='bilinear')
plt.axis("off")
plt.show()

#Outputting to csv
with open("CanonCL.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(dailyitems)
