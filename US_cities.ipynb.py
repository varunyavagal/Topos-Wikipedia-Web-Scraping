# -*- coding: utf-8 -*-
"""
Created on Sat May 25 17:23:48 2019

@author: varun
"""

import pandas as pd
import wikipedia
import time
from selenium import webdriver
from pandas import ExcelWriter
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import requests
from wikipedia import DisambiguationError, PageError

"""Srapped data container list variables declaration"""
sr_no_list=[]
city_list=[]
state_list=[]
pop_2018_list=[]
pop_2010_list=[]
pop_change_list=[]
area_2016_sqml_list=[]
area_2016_sqkm_list=[]
pop_density_2016_sqml_list=[] 
pop_density_2016_sqkm_list=[]
city_loc_list=[]
city_summary_list=[]
city_gov_list=[]


"""URL of website"""
url=r'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'


"""Start timer"""
Start_time= time.time()

""" get url"""

driver=webdriver.Chrome()
driver.get(url)

for i in range(1,315,1):
    #Sr. No.
    sr_no_list.append(i)

    #City   
    
    city_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[2]/i/a'
    try:
        city=driver.find_element_by_xpath(city_xpath).text
    except NoSuchElementException:
        try: 
            city_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[2]/i/b/a'
            city=driver.find_element_by_xpath(city_xpath).text
        except NoSuchElementException :
            try:
                city_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[2]/a'
                city=driver.find_element_by_xpath(city_xpath).text
            except NoSuchElementException :
                try:
                    city_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[2]/b/a'
                    city=driver.find_element_by_xpath(city_xpath).text
                except :
                    print(" Exception occured at city with sr no.{0} ".format(i) )
        
    city_list.append(city)
    
    #State
    state_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[3]/a'
    try:
        State=driver.find_element_by_xpath(state_xpath).text
    except NoSuchElementException:
        try:
            state_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[3]'
            State=driver.find_element_by_xpath(state_xpath).text
        except NoSuchElementException:
            print(" Exception oocured at state with sr no. {0} " .format(i) )
    state_list.append(State)
    
    #Population of city in 2018
    pop_2018_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[4]'
    pop_2018=driver.find_element_by_xpath(pop_2018_xpath).text
    pop_2018_list.append(pop_2018)

    #Population of city in 2010
    pop_2010_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[5]'
    pop_2010=driver.find_element_by_xpath(pop_2010_xpath).text
    pop_2010_list.append(pop_2010)

    #Population change of city from 2010 to 2018    
    pop_change_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[6]'
    pop_change=driver.find_element_by_xpath(pop_change_xpath).text
    pop_change_list.append(pop_change)

    #City area in Square Miles
    area_2016_sqml_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[7]'
    area_2016_sqml=driver.find_element_by_xpath(area_2016_sqml_xpath).text
    area_2016_sqml_list.append(area_2016_sqml)
    
    #City area in Square KM
    area_2016_sqkm_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[8]'
    area_2016_sqkm=driver.find_element_by_xpath(area_2016_sqkm_xpath).text
    area_2016_sqkm_list.append(area_2016_sqkm)

    #Population density of city in per square miles
    pop_density_2016_sqml_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[9]'
    pop_density_2016_sqml=driver.find_element_by_xpath(pop_density_2016_sqml_xpath).text
    pop_density_2016_sqml_list.append(pop_density_2016_sqml)
    
    #Population density of city in per square KM
    pop_density_2016_sqkm_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[10]'
    pop_density_2016_sqkm=driver.find_element_by_xpath(pop_density_2016_sqkm_xpath).text
    pop_density_2016_sqkm_list.append(pop_density_2016_sqkm)
     
    #Location coordinates of city 
    city_loc_xpath='//*[@id="mw-content-text"]/div/table[5]/tbody/tr['+str(i)+']/td[11]'
    city_loc=driver.find_element_by_xpath(city_loc_xpath).text
    city_loc_list.append(city_loc)
    
    """ Entering into the city page"""
    #city summary
    try:
        city_summary=wikipedia.summary(city)
    except DisambiguationError: 
        try:
            city= city+", " + State
            city_summary=wikipedia.summary(city)
        except PageError:
                 city= city+", " + State
                 city_summary= "NA"
                 
    city_summary_list.append(city_summary)
   
    print(i)

'''Consolidation of all list into pandas dataframe'''
           
df1 = pd.DataFrame(sr_no_list, columns=['Sr No'])
df2=pd.DataFrame(city_list, columns=['City'])
df3=pd.DataFrame(state_list, columns=['State'])
df4=pd.DataFrame(pop_2010_list, columns=['Population in 2010'])
df5=pd.DataFrame(pop_2018_list, columns=['Population in 2018'])
df6=pd.DataFrame(pop_change_list, columns=['Change in Population'])
df7=pd.DataFrame(area_2016_sqml_list, columns=['City Area (SQML)'])
df8=pd.DataFrame(area_2016_sqkm_list, columns=['City Area (SQKM)'])
df9=pd.DataFrame(pop_density_2016_sqml_list, columns=['Population Density/ SQ.ML'] )
df10=pd.DataFrame(pop_density_2016_sqkm_list, columns=['Population Density/ SQ.KM'] )
df11=pd.DataFrame(city_loc_list, columns=['City Location'] )
df12=pd.DataFrame(city_summary_list, columns=['Summary'] )

df_12=df1.join(df2)
df_123=df_12.join(df3)
df_1234=df_123.join(df4)
df_12345=df_1234.join(df5)
df_123456=df_12345.join(df6)
df_1234567=df_123456.join(df7)
df_12345678=df_123456.join(df8)
df_123456789=df_12345678.join(df9)
df_01=df_123456789.join(df10)
df_02=df_01.join(df11)
df_03=df_02.join(df12)

"""Dataframe to CSV""" 
df_03.to_csv(r'US cities.csv', index=False)

"""To XLSV """
writer = ExcelWriter('USA Cities' + '.xlsx')
df_03.to_excel(writer, 'Sheet1', index=False)
writer.save()   

elapsed_time=time.time()- Start_time
print(elapsed_time)


