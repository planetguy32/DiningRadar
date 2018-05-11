#  scraper.py  #
#  This file scrapes the nutrition

from bs4 import BeautifulSoup
import requests
import re

r = requests.get("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=UC+Santa+Cruz+Dining&dtdate=05%2F06%2F2018&locationNum=05&locationName=Cowell+Stevenson+Dining+Hall&naFlag=1")
base_url = "http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=UC+Santa+Cruz+Dining&dtdate=<date>&locationNum=<loc_num>&locationName=<loc_name>&naFlag=1"


# The 'nutrition info' words appear just after each menu section so we know their indexes
# Returns 'clean list' rid of the 'nutrition info' words
def clean_list(food_list):
    nutr_indexes = [food_list.index('Breakfast') + 1, food_list.index('Lunch') + 1,
                    food_list.index('Dinner') + 1, food_list.index('Late Night') + 1]

    clean_list = [item for item in food_list if food_list.index(item) not in nutr_indexes]
    return clean_list

# Assembles the menu dictionary:
#   Adds new key if food time encountered
#   Appends to list under current food time if food item
# Input: A list of food items and food times
# Returns a dictionary -- each key is menu times, value is an inner dictionary of menu items available at that time
#                                                   value of inner dictionary is list of food preferences (allergies)

def make_food_dict(food_list, soup):
    section_indexes = [food_list.index('Breakfast'), food_list.index('Lunch'),
                       food_list.index('Dinner'), food_list.index('Late Night')]

    items_dict = {}
    food_section = None
    for i in range(len(food_list)):
        if i in section_indexes:
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
        final_word = "The nutrient composition of food may vary due to genetic, " \
                     "environmental and processing variables; changes in product " \
                     "formulation, manufacturer's data, cooking and preparation techniques. " \
                     "The information provided in these labels should be considered " \
                     "as approximations of the nutritional analysis of the food."

        food_items_begin = stripped_words.index('Breakfast')
        food_items_end = stripped_words.index(final_word)
        # Constructs a list of all food items but also includes random nutrition_info words which we have to clean up
        food_items_dirty = stripped_words[food_items_begin:food_items_end]

        food_items_clean = clean_list(food_items_dirty)
        menu_dict = make_food_dict(food_items_clean, soup)

        return menu_dict


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
date = dict(month="05", day="06", year="2018")
print(get_menu(date, "Cowell Stevenson Dining Hall"))



