import time

import requests
import re
from bs4 import BeautifulSoup

# Base url for querying
nutrition_base_url = "http://nutrition.sa.ucsc.edu/pickMenu.asp?locationNum=<loc_num>&locationName=<loc_num>&dtdate=<date>&mealName=<meal>&sName=UC+Santa+Cruz+Dining"

# Try to clean up the string, if any errors are encountered then
#   the food item most likely has no nutritional information
def clean(string_list):
    try:
        string_list = clean_dv(string_list)
        string_list = clean_end(string_list)
        string_list = clean_dashes(string_list)
        string_list = clean_percent(string_list)
        string_list = expand_acros(string_list)
        string_list = split_calories(string_list)
    except ValueError as e:
        print(e)
        string_list = []
    return string_list

# Removes strings from list which include the "- - - g" phrase
#   indicating missing values
def clean_dashes(string_list):
    new_list = []
    for string in string_list:
        if string.find("- - - g") == -1 and string.find("- - - mg") == -1:
            new_list.append(string)
    return new_list

# Remove unnecessary DV labels
def clean_dv(string_list):
    dv_start = string_list.index('*Percent Daily Values (DV)')
    dv_end = len(string_list) - 1 - string_list[::-1].index('%DV*')
    return [string for string in string_list if
            string_list.index(string) < dv_start or
            string_list.index(string) > dv_end]


# Prune off uninformative elements at end of list
def clean_end(string_list):
    final_index = string_list.index("ALLERGENS:") + 1
    return string_list[:final_index+1]

# Remove standalone d.v. percentages as they reoccur later in the list
def clean_percent(string_list):
    return [string for string in string_list if
            string != '%' and #something not working in line below
            string_list[(string_list.index(string)+1) % len(string_list)] != '%']

# Expand the acronyms sat. fat and tot. carb to keep consistency across naming
def expand_acros(string_list):
    for string in string_list:
        if string == "Sat. Fat":
            string_list[string_list.index(string)] = "Saturated Fat"
        if string == "Tot. Carb.":
            string_list[string_list.index(string)] = "Carbohydrates"
    return string_list

# Split calories and their values into seperate list items
#   to help with adding to a dictionary
def split_calories(string_list):
    new_string_list = []
    for string in string_list:
        if string.find("Calories from") != -1:
            cals_split = string.split(" ")
            new_string_list.append(" ".join(cals_split[:-1]))
            new_string_list.append(cals_split[-1:][0])
        elif string.find("Calories ") != -1:
            cals_split = string.split(" ")
            new_string_list.append(" ".join(cals_split[:-1]))
            new_string_list.append(cals_split[-1:][0])
        elif string.find("Calories") != -1:
            # Remove final calories (never followed by a value)
            pass
        else:
            new_string_list.append(string)
    return new_string_list




# Returns true if word contains at least one numeric character
def contains_numeric(word):
    for letter in word:
        if letter.isnumeric():
            return True
    return False

# Remove any items that don't have associated values
def clean_empty_categories(string_list):
    new_list = string_list[:3]
    x = 3
    while x+1 < len(string_list):
        if not (contains_numeric(string_list[x+1]) and
                string_list[x+1] != "Vitamin B12"):
                x -= 1
                break
        else:
            new_list.append(string_list[x])
            new_list.append(string_list[x + 1])

        x += 2
    return new_list




# Takes in the list of items
# Returns three items
# - inputted list with only quantity/d.v. values
# - ingredients
# - allergens
def get_info(string_list):
    ingredients = string_list[string_list.index("INGREDIENTS:") + 1]
    allergens = string_list[string_list.index("ALLERGENS:") + 1]
    new_list = string_list[:-4]
    return new_list, ingredients, allergens


# Takes in the list of items assembles a dictionary of nutritional values
def assemble_nutrition(item_list, nutrition_dict):
    item_name = item_list[1]
    nutrition_list = item_list[5:]
    nutrition_dict[item_name] = {}
    nutrition_dict[item_name]['Serving Size'] = item_list[4]

    for x in range(0, len(nutrition_list), 2) :
        item = nutrition_list[x]
        if item not in nutrition_dict[item_name]:
            nutrition_dict[item_name][item] = nutrition_list[x+1]
    return nutrition_dict


# Takes in the url of the nutrition information and appends info to nutrition dictionary
def get_nutrition(url, nutrition_dict):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    string_list = []
    for string in soup.stripped_strings:
        string_list.append(string.replace(u'\xa0', u' '))
    cleaned_list = clean(string_list)
    nutrition_info = nutrition_dict
    if cleaned_list:
        leftover_list, ingredients, allergens = get_info(cleaned_list)
        leftover_list = clean_empty_categories(leftover_list)
        nutrition_info = assemble_nutrition(leftover_list, nutrition_dict)
    return nutrition_info

# Take in date object and location name and return dictionary of all
#   nutrition information
def all_nutrition(date, locationName):
    meal_times = ["Breakfast", "Lunch", "Dinner", "Late Night"]
    locationNum = get_location_num(locationName)
    if locationNum == "-1":
        print("BAD LOCATION NAME")
    else:
        nutrition_dict = {}
        for meal in meal_times:
            url = get_nutrition_url(date, locationNum, locationName, meal)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links[:-1]:
                full_url = "http://nutrition.sa.ucsc.edu/" + link['href']
                nutrition_dict = get_nutrition(full_url, nutrition_dict)
    return nutrition_dict

# Builds the nutrition url from the appropriate inputs
def get_nutrition_url(date, locationNum, locationName, mealTime):
    date_string = date['month'] + "%2F" + date['day'] + "%2F" + date['year']
    locationName = re.sub(' ', '+', locationName)
    locationName = re.sub('and', '%26', locationName)  # replace the 'and' in College Nine and Ten with html code
    mealTime = re.sub(' ', '+', mealTime)
    nutrition_url = re.sub('<date>', date_string, nutrition_base_url)
    nutrition_url = re.sub('<loc_num>', locationNum, nutrition_url)
    nutrition_url = re.sub('<loc_name>', locationName, nutrition_url)
    nutrition_url = re.sub('<meal>', mealTime, nutrition_url)
    return nutrition_url


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


diningHallNames = ["Cowell Stevenson Dining Hall",
    "Crown Merrill Dining Hall",
    "Porter Kresge Dining Hall",
    "Rachel Carson Oakes Dining Hall",
    "Colleges Nine and Ten Dining Hall"]


""" TESTING
for days_ahead in range(0, 10):
    time_object = time.localtime(time.time()+days_ahead * 86400)
    for location in diningHallNames:
        menu=menu_scraper.get_menu(dict(month=str(time_object.tm_mon), day=str(time_object.tm_mday), year=str(time_object.tm_year)), location)
        nutrition=all_nutrition(dict(month=str(time_object.tm_mon), day=str(time_object.tm_mday), year=str(time_object.tm_year)),
                                                  location)
        for meal, foods in menu.items():
            for food, dietary_info in foods.items():
                nutrition_info=nutrition.get(food)
                if nutrition_info:
                    print(nutrition_info.get('Calories'))

date = dict(month="06", day="10", year="2018")
print(all_nutrition(date, "Rachel Carson Oakes Dining Hall"))

"""