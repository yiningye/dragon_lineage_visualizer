from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
from lineage_helper import DragonNode, serialize_tree
import math


def calculate_portrait_url(dragon_id):
    portrait_id = math.ceil(dragon_id/100)
    if (dragon_id % 100 == 0):
        portrait_id += 1;

    return 'http://flightrising.com/rendern/portraits/' + portrait_id + '/' + dragon_id + 'p.png'

def fetch_dragon_metadata(dragon_id, driver):
    dragon_url = 'https://www1.flightrising.com/dragon/'+dragon_id
    driver.get(dragon_url)
    wait = WebDriverWait(driver, 10)
    html = driver.page_source
    
    name = "Random-Name"
    gender = "F"
    dragon_id = 333
    flight = "Arcane"
    portrait_url = calculate_portrait_url(dragon_id)
    num_descendants = 0
    return DragonNode(dragon_id, name, gender, flight, portrait_url)

def fetch_dragon_lineage(root_dragon_id, max_generations=3):
    if max_generations > 5:
        print("Risk of visualization being too cluttered")
        #  Send message to frontend
    else:
        
        # Set up Selenium WebDriver
        driver = webdriver.Chrome()
        root = fetch_dragon_metadata(root_dragon_id, driver)
        


    

        driver.quit()
    
    
    

        # Convert the data into a json and send to frontend
        
        print(f"Dragon lineage saved in json")


fetch_dragon_lineage(9895, 4)
