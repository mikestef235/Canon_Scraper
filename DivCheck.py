from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
from bs4 import BeautifulSoup
import urllib
import urllib.request
import html.parser
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar
import http.cookiejar
import csv
from csv import reader
import time
import re
import os

# Starting the Webcrawler, this part won't change-------------------------
driver = webdriver.Chrome()
driver.get("http://yates.sdgnys.com/index.aspx")
elem1 = driver.find_element_by_link_text("Click Here for Public Access")
elem1.click()

# Time to go through the second page
nextURL = driver.current_url
driver.get(nextURL)
driver.find_element_by_xpath(".//*[contains(text(), 'I agree')]").click()
driver.find_element_by_name("btnSubmit").click()
#-------------------------------------------------------------------------

# Time to go through the search page (Inputing East Bluff DR)
nextURL = driver.current_url
streetInput = driver.find_element_by_name("txtStreetName")
streetInput.send_keys("East Lake Rd")
streetInput.send_keys(Keys.ENTER)
#-------------------------------------------------------------------------

# Printing all of the first page table
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Find the number of pages for this street
pgstr = driver.find_element_by_id("lblPageCount2").text
pgs = int(pgstr)
pgloop = list(range(pgs))

# Need to insert here for pages!!!!!!!!!!!!!!


# Printing all links on the first page
    html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
table = soup.find('table', 'reportTable')
links = table.findAll('a')
del links[0:5]

# Going into the stored links and getting the data
pageProperties = ""
pageOwners = ""
pageSales = ""
pgNum += 1
count = 0


# Clicking the property link
st = link.string
driver.find_element_by_xpath(".//*[contains(text(), '%s')]" % st).click()

# Finding the property data table
html = driver.page_source
soupProp = BeautifulSoup(html, "html.parser")
divTest = soupProp.find("div", {'id': "pnlRTaxID"})
divTable = divTest.find("table")

# Creating the property data table
rows = divTable.findChildren(['th', 'tr'])

# Going through the contents of each cell
propData = ""
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        if cell.string is None:
            propData = propData + ",BLANK"
            continue
        elif '$' in cell.string:
            continue
        else:
            propData = propData + "," + cell.string

# Removing the first comma
propData = propData[1:]

# Converting to a list
propData = propData.split(",")
# Getting rid of exception words
exceptionWords = [
    "Status",
    "Roll Section:",
    "Address:",
    "Property Class:"
    "Ownership Code:",
    "Site:",
    "In Ag. District:",
    "Zoning Code:",
    "Bldg. Style:"
    "Neighborhood:",
    "School District:",
    "Total Acreage/Size:",
    "Equalization Rate:"
    "Land Assessment:",
    "Total Assessment:",
    "Full Market Value:",
    "BLANK"
    "Deed Book:",
    "Deed Page:",
    "Grid East:",
    "Grid North:"]
propFinal = []
for i in list(range(len(propData))):
    if propData[i] not in exceptionWords:
    propFinal.append(propData[i])

# Appending the property values
landAssess = soupProp.find("span", {'id': 'lblLandAssess'}).get_text()
landAssess = landAssess.replace('2017 - $', '')
landAssess = '"' + landAssess + '"'
print(landAssess)
fullAssess = soupProp.find("span", {'id': 'lblTotalAssess'}).get_text()
fullAssess = fullAssess.replace('2017 - $', '')
fullAssess = '"' + fullAssess + '"'
print(fullAssess)
totalAssess = soupProp.find("span", {'id': 'lblFullMarketValue'}).get_text()
totalAssess = totalAssess.replace('2017 - $', '')
totalAssess = '"' + totalAssess + '"'
print(totalAssess)
propFinal.append(landAssess)
propFinal.append(fullAssess)
propFinal.append(totalAssess)
# Adding a record number
propData = str(count + 1 + 100 * (pgNum - 1)) + ',' + propData
