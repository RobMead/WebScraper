from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url = "https://results.prudentialridelondon.co.uk/2018/?pid=search"
# initialise selenium Chrome webdriver and pass the webdriver the ride london url
driver = webdriver.Chrome()
driver.get(url)

# flag for while loop
flag = 0

while(flag == 0):
    # create BeautifulSoup obect based on page source code
    soup_level1=BeautifulSoup(driver.page_source,'lxml')

    #find all tags which provide rider's name and add them
    #to a list
    name = []
    for link in soup_level1.find_all("h4","type-fullname"):
        name.append(link.text)
        
    # find the finish time tag and add the parent tag's text
    # to a list
    finish = []
    for link in soup_level1.find_all("div",string="Finish"):
        finish.append(link.parent.get_text(" "))
    # pop the first item since not a valid result
    finish.pop(0)

    # same as for finish time except with 'distance'
    distance=[]
    for link in soup_level1.find_all("div",string="Distance"):
        distance.append(link.parent.get_text(" "))
    distance.pop(0)

    # zip name, finish time & distance together into single
    # list
    zips = []
    for item in zip(name,distance,finish):
        zips.append(item)

    # convert zips list into numpy array
    zips = np.array(zips)
    # convert into pandas dataframe and output to csv
    df = pd.DataFrame(zips)
    with open('out.csv','a') as f:
        df.to_csv(f, header=False)

    # navigate to next page using next page's navigation 
    # text '>'. If doesn't exist, then it's the last page
    # so exit the loop
    try:
        next_page = driver.find_element_by_link_text('>')
        next_page.click()
    except:
        flag = 1

driver.quit()
