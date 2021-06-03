from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
import time
from selenium.webdriver.firefox.options import Options
start_time = time.time()

#read in dataset to get brand keywords
df = pd.read_excel(r"C:\Users\mxr29\Desktop\Computer\APA_bou.xlsx", sheet_name='Sheet1')

#was xpath list but now Key phrase list
xpath_list = [ 'Accessories'
               ,
          'Bags',
          'Dresses',
          'Intimates',
          'Jackets',
          'Jeans',
          'Jewelry',
          'Pants',
          'Shoes',
          'Shorts',
          'Skirts',
          'Sweaters',
          'Swim',
          'Tops'
              ]

#intialize list than make list of list for price ranges
brand_list = []
Accessories = []
Bags = []
Dresses = []
Intimates = []
Jackets = []
Jeans = []
Jewelry = []
Makeup = []
Pants = []
Shoes = []
Shorts = []
Skirts = []
Sweaters = []
Swim =[]
Tops = []
Skincare = []
Hair = []
Bath = []


price_list = [
    Accessories,Bags,Dresses,Intimates,Jackets,
    Jeans,Jewelry,Makeup,Pants,Shoes,Shorts,
    Skirts,Sweaters,Swim,Tops,Skincare,Hair,Bath
]

##intialize list than make list of list for item counts
Accessories_c = []
Bags_c = []
Dresses_c = []
Intimates_c = []
Jackets_c = []
Jeans_c = []
Jewelry_c = []
Makeup_c = []
Pants_c = []
Shoes_c = []
Shorts_c = []
Skirts_c = []
Sweaters_c = []
Swim_c =[]
Tops_c = []
Skincare_c = []
Hair_c = []
Bath_c = []

count_list =[
    Accessories_c,Bags_c,Dresses_c,Intimates_c,Jackets_c,Jeans_c,
    Jewelry_c,Makeup_c,Pants_c,Shoes_c,Shorts_c,Skirts_c,Sweaters_c,
    Swim_c,Tops_c,Skincare_c,Hair_c,Bath_c
]

#first loop iterates through each brand name
for p in range(480,len(df)):


    # grab and clean brand name
    brand = df['Boutique Brands'].iloc[p]
    try:
        brand = (str(brand).split('('))[0]
    except:
        pass

    brand_list.append(brand)

    #iterate through each of the key phrase for item type
    for y in range(len(xpath_list)):
        # bool variable to check if type of brand is present
        type_bool = True

        #open headless browser for automation then sleep to load
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\mxr29\Desktop\Computer\Drivers\geckodriver.exe')
        driver.get("https://poshmark.com/search?query= ")
        sleep(3)

        #find the brand search bar,input brand,click search, and sleep to load
        brand_enter = driver.find_element_by_xpath(
            '//*[@id="searchInput"]')
        brand_enter.clear()
        brand_enter.send_keys(str(brand))
        search = driver.find_element_by_xpath('/html/body/div[1]/header/nav[1]/div/div[1]/form/div[1]/button')
        search.click()
        sleep(3)

        #slect the women's clothing group and click
        women = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div/div/div/div[2]/nav/div/div[1]/div/div[2]/ul/li[2]/a')
        women.click()
        sleep(3)

        #intiliase M value for keep, Price, and Count for Brand Type
        keep = 100000
        price = []
        count = 0

        #Since the brand types can be in dynamic numeric positions this loop find the xpath numeric position for the current brand
        #and keeps that number so we can get the correct xpath.
        for i in range(1, 19):

            try:
                #grab keyword clean up and check if the index should be kept.
                index_list = driver.find_element_by_xpath(
                    '/html/body/div[1]/main/div[2]/div/div/div/div[2]/nav/div/div[1]/div/div[2]/ul/li[2]/ul/li[' + str(
                        i) + ']/a')
                keyword = (index_list.get_attribute('innerHTML'))
                keyword = (keyword.split(' '))
                keyword = (keyword[10])
                keyword = keyword.splitlines()[0]
                if keyword == xpath_list[y]:
                    keep = i
            except:
                pass

        # this segment trys to click the element specified on the indexed found in the previous search loop
        # if fails sets type bool to false which skips the price searching portion
        try:
            enter1 = driver.find_element_by_xpath(
                '/html/body/div[1]/main/div[2]/div/div/div/div[2]/nav/div/div[1]/div/div[2]/ul/li[2]/ul/li[' + str(
                    keep) + ']/a')
            enter1.click()
            sleep(3)
        except:
            type_bool = False

        # this segement loops through pages and collects prices until it runs out of pages if type_bool is True
        if type_bool == True:

            #bool for page search goes though 8 pages or if no more pages exist
            page_bool = True
            z = 1
            while (page_bool == True):
                if z ==8:
                    page_bool = False

                #grabs all prices and names on current page
                prices = driver.find_elements_by_css_selector(".p--t--1.fw--bold")
                name  = driver.find_elements_by_css_selector(".tile__title.tc--b")

                #loops through all elements on page
                for i in range(len(prices)):

                    #checks if brand name is in item name str
                    if brand in str(name[i].get_attribute('innerHTML')):
                        #cleans price
                        value = (str(prices[i].get_attribute('innerHTML')))
                        value = (value.split('$'))[1]
                        value = value.splitlines()[0]
                        try:
                            price.append(int(value))
                            count += 1
                        except:
                            pass
                #attempt to go to next page
                try:
                    box = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div/div/div/div[2]/section/div[3]/div[49]/button[2]')
                    box.click()
                    sleep(3)
                    z+=1
                except:
                    page_bool = False



        #attempts to take the price list and turn into a range of 25th percentile and 75th percentile
        #if fails appends with an X
        try:
            price_list[y].append(str((round(np.percentile(price,25)))) +'-'+ str(round(np.percentile(price,75))))
            count_list[y].append(count)
        except:
            price_list[y].append('X')
            count_list[y].append(0)

        driver.quit()

    #after every brand loop remake and save dataframe.
    # Kind of inefficient but that way I don't lose the whole data set half way through if faced with an error
    print(brand)
    print(p)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('*******************************************************************')

    df_out = pd.DataFrame({ 'Brand': brand_list})
    for i in range(len(xpath_list)):
        df_out[xpath_list[i]]=price_list[i]
    for i in range(len(xpath_list)):
        df_out[str(xpath_list[i])+' Count']=count_list[i]
    df_out.to_csv(r'C:\Users\mxr29\Desktop\Computer\poshtest_480_X.csv')
