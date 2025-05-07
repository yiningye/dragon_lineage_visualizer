from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
# import pandas as pd
import requests
import os
from datetime import datetime, timedelta
from lineage_helper import DragonNode, serialize_tree
import math
from collections import deque


def calculate_portrait_url(dragon_id):
    print(dragon_id)
    portrait_id = math.ceil(dragon_id/100)
    if (dragon_id % 100 == 0):
        portrait_id += 1;

    return 'http://flightrising.com/rendern/portraits/' + str(portrait_id) + '/' + str(dragon_id) + 'p.png'

def clan_flight(banner_img_link):
    # Example img link: /static/cms/location_banners/34.jpg
    banner_number = int(banner_img_link.split("/")[-1].split(".")[0])
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
    

def fetch_dragon_metadata(dragon_node, dragon_id, driver):
    dragon_url = 'https://www1.flightrising.com/dragon/'+str(dragon_id)
    driver.get(dragon_url)
    wait = WebDriverWait(driver, 10)
    html = driver.page_source
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    #Clan Flight
    banner_div = soup.find("div", class_="banner", role="banner")
    if banner_div:
        style = banner_div.get("style", "")
        # Extract the URL using string operations
        start = style.find("url(")
        end = style.find(")", start)
        if start != -1 and end != -1:
            image_url = style[start + 4:end].strip("'\"")
        else:
            print("URL not found in style.")
    else:
        print("Banner div not found.")
    flight = clan_flight(image_url)
    
    # #Name
    name_h1 = soup.find("h1", class_="dragon-profile-header-name", id="main-content")
    if name_h1:
        name = name_h1.get_text(strip=True)
    else:
        print("Name header not found.")
    
    #Gender
    gender_div = soup.find("div", id = "dragon-profile-icon-sex-tooltip") 

    if gender_div:
        print("gender div found")
        strong_gender =  gender_div.find("strong")
        if strong_gender:
            print("strong found")

            gender = strong_gender.text
        else:
            print("Gender text not found.")
    else:
        print("Gender tooltip div not found.")    
        
    dragon_node.update_metaData(name, gender, flight)
    print(name, dragon_id, gender, flight)

def fetch_dragon_lineage(root_dragon_id, max_generations=3):
    if max_generations > 5:
        print("Risk of visualization being too cluttered")
        #  Send message to frontend
    else:
        #Traversal algorithm
        
        # Set up Selenium WebDriver
        driver = webdriver.Chrome()
        rootNode = DragonNode(root_dragon_id)
        root = fetch_dragon_metadata(rootNode, root_dragon_id, driver)
        # queue = []
        # queue.append((root, 1))  # store (node, current_level)

        # while queue:
        #     node, level = queue.popleft()
            
        #     if level > max_levels:
        #         break
            
        #     print(f"Level {level}: {node.value}")  # Or whatever processing you need
            
        #     if node.left:
        #         queue.append((node.left, level + 1))
        #     if node.right:
        #         queue.append((node.right, level + 1))

        # Convert the data into a json and send to frontend
        
        print(f"Dragon lineage saved in json")
        driver.quit()


fetch_dragon_lineage(9895, 4)
