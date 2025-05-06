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

def which_flight(banner_img_link):
    # Example img link: https://www1.flightrising.com/static/cms/location_banners/5.jpg
    banner_number = banner_img_link.split("/")[-1].split(".")[0]
    
    if banner_number == 1 or banner_number == 2:
        return "Earth"
    elif banner_number == 41 or banner_number == 42:
        return "Fire"
    elif banner_number == 9 or banner_number == 10:
        return "Wind"
    elif banner_number == 13 or banner_number == 14:
        return "Water"
    elif banner_number == 25 or banner_number == 26:
        return "Shadow"
    elif banner_number == 21 or banner_number == 22:
        return "Ice"
    elif banner_number == 17 or banner_number == 18:
        return "Lightning"
    elif banner_number == 29 or banner_number == 30:
        return "Light"
    elif banner_number == 37 or banner_number == 38:
        return "Nature"
    elif banner_number == 5 or banner_number == 6:
        return "Plague"
    elif banner_number == 33 or banner_number == 34:
        return "Arcane"
    else:
        return "Unknown"
    

def fetch_dragon_metadata(dragon_id, driver):
    dragon_url = 'https://www1.flightrising.com/dragon/'+dragon_id
    driver.get(dragon_url)
    wait = WebDriverWait(driver, 10)
    html = driver.page_source
    
    # Parse updated HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "IncrementGridView_DXMainTable"})
    
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
