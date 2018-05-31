import random
import requests
import datetime


def search():
    food=request.vars.food_name

    query = (db.available_food.food_id == db.menu_item.id)

    #Filter by food name
    query = query & db.menu_item.menu_name.contains(food)

    #Filter by dietary restrictions
    possible_dietary_restrictions = ['eggs', 'fish', 'gluten_free', 'dairy', 'nuts', 'soy', 'vegan', 'vegetarian', 'pork', 'beef', 'halal']
    for s in possible_dietary_restrictions:
        s="menu_is_"+s
        if s in request.vars:
            query = query & (db.menu_item[s] == (request.vars[s] == "T"))


    #Filter by dining hall restrictions
    possible_dining_halls = {
            'crown_merrill': "Crown Merrill Dining Hall",
            'porter_kresge':"Porter Kresge Dining Hall",
            'carson_oakes': "Rachel Carson Oakes Dining Hall",
            'cowell_stevenson': "Cowell Stevenson Dining Hall",
            'nine_ten': "Colleges Nine and Ten Dining Hall" }
    subQuery = None
    for hall, realName in possible_dining_halls.iteritems():
        if hall in request.vars:
            print("Requested dining hall: "+hall)
            a=(db.available_food.food_location == realName)
            if subQuery == None:
                subQuery=a
            else:
                subQuery = subQuery | a
    if subQuery <> None:
        query = query & subQuery


    selection=db(query).select(db.menu_item.menu_name, db.available_food.food_location, db.available_food.food_meal
    ##TODO is getting dates from a DB possible in Web2Py?
##              , db.available_food.food_date
              )
    results=[]
    for a in selection:
        results.append(
            {"name": a.menu_item.menu_name,
             "hall": a.available_food.food_location,
             "meal": a.available_food.food_meal,
    ##TODO is getting dates from a DB possible in Web2Py?
##             "time_to": a.available_food.food_date.date()-datetime.datetime.today()
            })
    return response.json(dict(results=results))
