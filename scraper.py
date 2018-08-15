from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
#import re
#import os

url = "https://results.prudentialridelondon.co.uk/2018/?pid=search"
driver = webdriver.Chrome()
driver.get(url)
flag = 0

while(flag == 0):
    soup_level1=BeautifulSoup(driver.page_source,'lxml')

    name = []
    for link in soup_level1.find_all("h4","type-fullname"):
        name.append(link.text)

    finish = []
    for link in soup_level1.find_all("div",string="Finish"):
        finish.append(link.parent.get_text(" "))
    finish.pop(0)

    distance=[]
    for link in soup_level1.find_all("div",string="Distance"):
        distance.append(link.parent.get_text(" "))
    distance.pop(0)

    zips = []
    for item in zip(name,distance,finish):
        zips.append(item)

    zips = np.array(zips)
    df = pd.DataFrame(zips)
    with open('out.csv','a') as f:
        df.to_csv(f, header=False)

    try:
        next_page = driver.find_element_by_link_text('>')
        next_page.click()
    except:
        flag = 1

driver.quit()
