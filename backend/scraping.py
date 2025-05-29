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
import json

def calculate_portrait_url(dragon_id):
    print(dragon_id)
    portrait_id = math.ceil(dragon_id/100)
    if (dragon_id % 100 == 0):
        portrait_id += 1;

    return 'http://flightrising.com/rendern/portraits/' + str(portrait_id) + '/' + str(dragon_id) + 'p.png'

def clan_flight_exalted(soup):
    # Example flight banner link: /static/cms/location_banners/34.jpg
    flight = "Unknown"
    exalted = False
    
    # Exalted
    if soup.find("div", class_="exalted-index", id="exalted-content"):
        print("exalted")
        exalted_details = soup.find("div", class_= "common-column exalted-details-column")
        deity = exalted_details.findAll("strong")[1].text
        if deity == "Plaguebringer":
            flight = "Plague"
        elif deity == "Lightweaver":
            flight = "Light"
        elif deity == "Flamecaller":
            flight = "Fire"
        elif deity == "Earthshaker":
            flight = "Earth"
        elif deity == "Tidelord":
            flight = "Water"
        elif deity == "Windsinger":
            flight = "Wind"
        elif deity == "Arcanist":
            flight = "Arcane"
        elif deity == "Icewarden":
            flight = "Ice"
        elif deity == "Stormcatcher":
            flight = "Lightning"
        elif deity == "Shadowbinder":
            flight = "Shadow"
        elif deity == "Gladekeeper":
            flight = "Nature"
        
        exalted = True
        return flight, exalted
    
    #Not Exalted
    exalted = False
    banner_div = soup.find("div", class_="banner", role="banner")
    if banner_div:
        style = banner_div.get("style", "")
        # Extract the URL using string operations
        start = style.find("url(")
        end = style.find(")", start)
        if start != -1 and end != -1:
            banner_img_link = style[start + 4:end].strip("'\"")
        else:
            print("URL not found in style.")
            return None, None
    else:
        print("Banner div not found.")
        return None, None
    
    
    banner_definer = banner_img_link.split("/")[-1].split(".")[0]
    print("banner_definer", banner_definer)
    
    banner_number = 0
    try:
        banner_number = int(banner_definer)
    except ValueError as ve:
        print("Exception: unrecognized banner", ve)
        #Send a message to frontend
        return
    
    if banner_number == 1 or banner_number == 2:
        flight = "Earth"
    elif banner_number == 41 or banner_number == 42:
        flight = "Fire"
    elif banner_number == 9 or banner_number == 10:
        flight = "Wind"
    elif banner_number == 13 or banner_number == 14:
        flight = "Water"
    elif banner_number == 25 or banner_number == 26:
        flight = "Shadow"
    elif banner_number == 21 or banner_number == 22:
        flight = "Ice"
    elif banner_number == 17 or banner_number == 18:
        flight = "Lightning"
    elif banner_number == 29 or banner_number == 30:
        flight = "Light"
    elif banner_number == 37 or banner_number == 38:
        flight = "Nature"
    elif banner_number == 5 or banner_number == 6:
        flight = "Plague"
    elif banner_number == 33 or banner_number == 34:
        flight = "Arcane"

    return flight, exalted
    

def update_dragon_metadata(dragon_node, soup):
    #Clan Flight
    flight, exalted = clan_flight_exalted(soup)
    
    # #Name
    if exalted:
        name_h1 = soup.find("h1", class_="content-header", id="main-content")
    else:
        name_h1 = soup.find("h1", class_="dragon-profile-header-name", id="main-content")
    if name_h1:
        name = name_h1.get_text(strip=True)
    else:
        print("Name header not found.")
    
    #Gender
    if exalted:
        gender = "Unknown"
    else:
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
            
    dragon_node.update_metaData(name, gender, flight, exalted)
    print(name, gender, flight, exalted)

def update_offspring_nodes(node, soup):
    if node.exalted:
        lineage_div = soup.find("div", class_= "common-column exalted-details-column")
        if lineage_div:
            offspring_list = lineage_div.findAll('ul', class_="exalted-lineage-list")[1]
            print("offspring_list", offspring_list)
        else:
            print("No offspring list for exalted dragon")
            return
    else:
        offspring_list = soup.find("ul", class_= "dragon-profile-lineage-offspring")
    
    offspring_generation = node.generation + 1
    children = []
    if offspring_list:
        for offspring in offspring_list.findAll('li'):
            print("offspring", offspring)
            link_item = offspring.find("a")
            if link_item:
                link = link_item['href']
                print("link", link)
                dragon_id = int(link.split("/")[-1])
                child_node = DragonNode(dragon_id, offspring_generation)
                children.append(child_node)
            elif offspring.find("em"):
                print("No children")
                break
            else:
                print("Unexpected offspring section")
        print("Added offspring.")
        node.children = children
        return children
    else:
        print("No offspring list.")
        return []
    
def remove_exalted(root_node):
    # Base case: if the current node is exalted, return None
    if root_node.exalted:
        print(root_node.name, "exalted child")
        return None

    print("is there filtering")
    # Filter the children recursively
    filtered_children = []
    for child in root_node.children:
        result = remove_exalted(child)
        if result is not None:
            filtered_children.append(result)
    
    root_node.children = filtered_children
    return root_node

def fetch_dragon_lineage(root_dragon_id, max_generations=2, exclude_exalted=False):
    if max_generations > 5:
        print("Risk of visualization being too cluttered")
        #  Send message to frontend
    else:
        #Traversal algorithm
        
        # Set up Selenium WebDriver
        driver = webdriver.Chrome()
        rootNode = DragonNode(root_dragon_id, 1)
        queue = []
        queue.append(rootNode)  
        while queue:
            node = queue.pop(0)
            if node.generation > max_generations:
                break
            dragon_url = 'https://www1.flightrising.com/dragon/'+str(node.dragon_id)
            driver.get(dragon_url)
            wait = WebDriverWait(driver, 10)
            html = driver.page_source
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(1)
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            
            #Update Node attributes
            update_dragon_metadata(node, soup)
                
                
            print(node.dragon_id, node.generation)
            if node.generation+1 <= max_generations:
                offspring = update_offspring_nodes(node, soup)
                for child_node in offspring:
                    queue.append(child_node)
        
        
        if exclude_exalted:
            if rootNode.exalted:
                #Send message to frontend
                print("Cannot exclude exalted dragons if root dragon is an exalted dragon") 
                return
            else: 
                rootNode = remove_exalted(rootNode)
        
        file_path = f"./data/dragon_{root_dragon_id}.json"

        
        # Convert the data into a json and send to frontend
        with open("./data/dragon_tree.json", 'w') as f:
            json.dump(serialize_tree(rootNode), f, indent=2)

        
        print(f"Dragon lineage saved in json")
        driver.quit()
        return rootNode


fetch_dragon_lineage(493, 2, False)

