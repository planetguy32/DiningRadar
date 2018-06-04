#  scraper.py  #
#  This file contains functions to scrape the dining hall menu for food items and their allergens

import datetime
from bs4 import BeautifulSoup
import requests
import re
from gluon.scheduler import Scheduler
import time
import exceptions
import traceback

#Test code
import sys, os

r = requests.get("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=UC+Santa+Cruz+Dining&dtdate=05%2F06%2F2018&locationNum=05&locationName=Cowell+Stevenson+Dining+Hall&naFlag=1")
base_url = "http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=UC+Santa+Cruz+Dining&dtdate=<date>&locationNum=<loc_num>&locationName=<loc_name>&naFlag=1"


# The 'nutrition info' words appear just after each menu section so we know their indexes
# Returns 'clean list' rid of the 'nutrition info' words
def clean_list(food_list):
    nutr_indices = []
    section_names = ['Breakfast', 'Lunch', 'Dinner', 'Late Night']

    for i in range(len(section_names)):
        if section_names[i] in food_list:
            nutr_indices.append(food_list.index(section_names[i]) + 1)

    clean_list = [item for item in food_list if food_list.index(item) not in nutr_indices]
    return clean_list

# Removes the escaped ampersand character, &amp
def clean_food_item(food_item):
    if '&amp;' in food_item:
        food_item = re.sub(r"&amp;", '&', food_item)
    return food_item

# Assembles the menu dictionary:
#   Adds new key if food time encountered
#   Appends to list under current food time if food item
# Input: A list of food items and food times
# Returns a dictionary -- each key is menu times, value is an inner dictionary of menu items available at that time
#                                                   value of inner dictionary is list of food preferences (allergies)

def make_food_dict(food_list, soup):
    section_indices = []
    section_names = ['Breakfast', 'Lunch', 'Dinner', 'Late Night']
    for i in range(len(section_names)):
        if section_names[i] in food_list:
            section_indices.append(food_list.index(section_names[i]))


    items_dict = {}
    food_section = None
    for i in range(len(food_list)):
        if i in section_indices:
            food_section = food_list[i]
            items_dict[food_section] = {}
        else:
            items_dict[food_section][food_list[i]] = []
    items_dict = add_preferences(items_dict, soup)
    return items_dict

# Traverses through html tree picking out each img tag -- associated with each preference/allergy image
# Get food item associated with preference and add each preference to the food dictionary
# Input: Item dictionary of foods, Soup of html tree
# Returns the updated item dictionary with each food item's preference added
def add_preferences(items_dict, soup):
    food_objects = set()
    for obj in soup.find_all('img'):
        food_blob = obj.parent.parent
        food_objects.add(food_blob)

    for obj in food_objects:
        food_item = re.findall(r"<span .*\">(.*)</span>", str(obj))[0]
        food_item = clean_food_item(food_item)
        food_preferences = re.findall(r"src=\"LegendImages/(.*).gif", str(obj))
        for menu_time in items_dict:
            for menu_item in items_dict[menu_time]:
                if food_item == menu_item:
                    for preference in food_preferences:
                        items_dict[menu_time][menu_item].append(preference)

    return items_dict



# Main function for getting menu
# Input:
# date: a dictionary with three keys --
#   month: 06 (two digits representing month)
#   day: 05 (two digits representing day)
#   year: 2018 (four digits representing year)
# locationName: the name of the dining hall must be chosen from the list below
#   Cowell Stevenson Dining Hall
#   Crown Merrill Dining Hall
#   Porter Kresge Dining Hall
#   Rachel Carson Oakes Dining Hall
#   Colleges Nine and Ten Dining Hall
# Returns a dictionary -- key = menu time, value = list of menu items available at time

def get_menu(date, locationName):
    locationNum = get_location_num(locationName)
    if locationNum == "-1":
        print("BAD LOCATION NAME")
    else:
        url = get_menu_url(date, locationNum, locationName)
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')

        stripped_words = []
        for string in soup.stripped_strings:
            stripped_words.append(string)

        # The final_word is the entry after the last food item
        final_word = ["The nutrient composition of food may vary due to genetic, " 
                      "environmental and processing variables; changes in product " 
                      "formulation, manufacturer's data, cooking and preparation techniques. " 
                      "The information provided in these labels should be considered " 
                      "as approximations of the nutritional analysis of the food.",
                      "Information is based on availability and subject to change. " 
                      "The nutrient composition of food may vary due to genetic, " 
                      "environmental and processing variables; changes in product " 
                      "formulation, manufacturer's data, cooking and preparation " 
                      "techniques. The information provided in these labels should " 
                      "be considered as approximations of the nutritional analysis of the food."]
        try:
            food_items_begin = stripped_words.index('Breakfast')
            food_items_end = None
            for word in final_word:
                if word in stripped_words:
                    food_items_end = stripped_words.index(final_word)
                else:
                    raise ValueError("Could not find meals")
            # Constructs a list of all food items but also includes random nutrition_info words which we have to clean up
            food_items_dirty = stripped_words[food_items_begin:food_items_end]

            food_items_clean = clean_list(food_items_dirty)
            menu_dict = make_food_dict(food_items_clean, soup)

            return menu_dict
        except ValueError as e:
            print(e)
            return {}


# Returns the formatted url to scrape
def get_menu_url(date, locationNum, locationName):
    date_string = date['month'] + "%2F" + date['day'] + "%2F" + date['year']
    locationName = re.sub(' ', '+', locationName)
    locationName = re.sub('and', '%26', locationName) #replace the 'and' in College Nine and Ten with html code
    menu_url = re.sub('<date>', date_string, base_url)
    menu_url = re.sub('<loc_num>', locationNum, menu_url)
    menu_url = re.sub('<loc_name>', locationName, menu_url)

    return menu_url

def get_location_num(locationName):
    if locationName == "Cowell Stevenson Dining Hall":
        return "05"
    if locationName == "Crown Merrill Dining Hall":
        return "20"
    if locationName == "Porter Kresge Dining Hall":
        return "25"
    if locationName == "Rachel Carson Oakes Dining Hall":
        return "30"
    if locationName == "Colleges Nine and Ten Dining Hall":
        return "40"
    return "-1"


## Example test
#date = dict(month="05", day="06", year="2018")
#print(get_menu(date, "Cowell Stevenson Dining Hall"))



def scrape_at_edge_of_range():
    scrape_to_db(10, 11)

#scheduler.queue_task(scrape_at_edge_of_range, period=86400)
#scheduler = Scheduler(db)

diningHallNames = ["Cowell Stevenson Dining Hall",
    "Crown Merrill Dining Hall",
    "Porter Kresge Dining Hall",
    "Rachel Carson Oakes Dining Hall",
    "Colleges Nine and Ten Dining Hall"]

def tend_db():
    # Nuke the old available_food DB
    db(db.available_food.id > -1).delete()
    # Scan the next 2 weeks
    scrape_to_db(0, 14)


def scrape_to_db(start, end):
    for days_ahead in range(start, end):
        time_object = time.localtime(time.time()+days_ahead * 86400)
        for location in diningHallNames:
#            log_to_file("===========================\n")
#            log_to_file(str(time_object)+"\n")
#            log_to_file(location+"\n")
#            log_to_file("---------------------------"+"\n")
            menu=get_menu(dict(month=str(time_object.tm_mon), day=str(time_object.tm_mday), year=str(time_object.tm_year)), location)
            for meal, foods in menu.items():
#                log_to_file(meal+"\n")
#                log_to_file(str(foods)+"\n")
                for food, dietary_info in foods.items():
#                    log_to_file(food+"\n")
                    foods_from_db = db(db.menu_item.menu_name == food).select(db.menu_item.id)
                    id=0
                    log_to_file(str(foods_from_db)+"\n")
                    if len(foods_from_db) == 0:
                        id=db.menu_item.insert(

#                            menu_is_ = "" in dietary_info,

                            menu_name = food.lower(),
                            menu_is_eggs = "eggs" in dietary_info,
                            menu_is_fish = "fish" in dietary_info,
                            menu_is_soy = "soy" in dietary_info,
                            menu_is_gluten_free = "gluten" in dietary_info,
                            menu_is_dairy = "milk" in dietary_info,
                            menu_is_nuts = "nuts" in dietary_info,
                            menu_is_vegan = "vegan" in dietary_info,
                            menu_is_vegetarian = "veggie" in dietary_info,
                            menu_is_pork = "pork" in dietary_info,
                            menu_is_beef = "beef" in dietary_info,
                            menu_is_halal = "halal" in dietary_info
                        )
                    else:
                        id=foods_from_db.first().id
                    db.available_food.insert(
                        food_id = id,
                        food_location = location,
                        food_date = days_ahead,
                        food_meal = meal
                    )
            #TODO put in DB
            #TODO db.commit() once all DB updates are done - in scheduler, this isn't automatic
    db.commit()

# For testing

def log_to_file(string):
    f= open("scraper.log","a+")
    f.write(string)


try:
    tend_db()
#    call(["zenity", "--info", '--text="Scraping succeeded"'])
#    call(["zenity", "--info", '--text=":)"'])
except Exception as error:
#    call(["zenity", "--info", '--text="Scraping failed"'])
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log_to_file("{0}\n{1}\n".format(str(exc_type), str(fname)))
    for s in traceback.format_tb(exc_tb):
            log_to_file("{0}".format(str(s)))
    #log_to_file("{0}\n".format(error))
#    call(["zenity", "--info", '--text="ow"'])



def scrape_at_edge_of_range():
    scrape_to_db(10, 11)

#scheduler.queue_task(scrape_at_edge_of_range, period=86400)

