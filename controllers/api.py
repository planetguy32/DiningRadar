import random
import requests
import datetime


def search():

    query = (db.available_food.food_id == db.menu_item.id)

    #Filter by food name
    if "food_name" in request.vars:
        food=request.vars["food_name"]
        query = query & db.menu_item.menu_name.contains(food)

    #Filter by dietary restrictions
    possible_dietary_restrictions = ['eggs', 'fish', 'gluten_free', 'dairy', 'nuts', 'soy', 'vegan', 'vegetarian', 'pork', 'beef', 'halal']
    for s in possible_dietary_restrictions:
        s="menu_is_"+s
        if s in request.vars:
            if(request.vars[s] == "1"):
                query = query & (db.menu_item[s] != (request.vars[s] == 1))
            elif(request.vars[s] == "-1"):
                query = query & (db.menu_item[s] == (request.vars[s] == -1))

    #Filter by dining hall locations
    possible_dining_halls = {
            'crown_merrill': "Crown Merrill Dining Hall",
            'porter_kresge':"Porter Kresge Dining Hall",
            'carson_oakes': "Rachel Carson Oakes Dining Hall",
            'cowell_stevenson': "Cowell Stevenson Dining Hall",
            'nine_ten': "Colleges Nine and Ten Dining Hall" }
    subQuery = None
    for hall, realName in possible_dining_halls.iteritems():
        if request.vars[hall] == 'true':
            print("Requested dining hall: "+ request.vars[hall])
            a=(db.available_food.food_location == realName)
            if subQuery == None:
                subQuery=a
            else:
                subQuery = subQuery | a
    if subQuery <> None:
        query = query & subQuery


    #Filter by dates
    if "latest_day_offset" in request.vars:
        end_date = int(request.vars["latest_day_offset"])
        start_date = 0
        if "earliest_day_offset" in request.vars:
            start_date = int(request.vars["earliest_day_offset"])
        query=query & (db.available_food.food_date <= end_date) & (db.available_food.food_date >= start_date)

    #order by specific values https://stackoverflow.com/questions/6332043/sql-order-by-multiple-values-in-specific-order
    selection=db(query).select(
                db.menu_item.menu_name
              , db.available_food.food_location
              , db.available_food.food_meal
              , db.available_food.food_date
              , orderby=(db.available_food.food_location
                        , db.available_food.food_date
                        , db.available_food.food_meal == 'Late Night'
                        , db.available_food.food_meal == 'Dinner'
                        , db.available_food.food_meal == 'Lunch'
                        , db.available_food.food_meal == 'Breakfast')
    #could be useful, label food on page w/ their allergens          , db.menu_item.menu_is_eggs
              )
    results=[]
    for a in selection:
        results.append(
            {"name": a.menu_item.menu_name,
             "hall": a.available_food.food_location,
             "meal": a.available_food.food_meal,
             "time_to": a.available_food.food_date
            })
    return response.json(dict(results=results))



@auth.requires_signature()
@auth.requires_login()
def add_search():
    t_id = db.saved_searches.insert(
        search_owner=auth.user_id,
        search_url=request.vars.search_url
    )
    t = db.notes(t_id)
    return response.json(dict(note=t))

@auth.requires_login()
def get_searches():
    logged_in = auth.user_id is not None
    searches = db(db.saved_searches.search_owner == auth.user_id).select(db.saved_searches.search_url, db.saved_searches.id)
    urls=[]
    for s in searches:
        urls.append(s)
    return response.json(urls)



@auth.requires_login()
@auth.requires_signature()
def remove_search():
    selection=db(db.saved_searches.id == request.vars.id)
    first=selection.select().first()
    if(first <> None and first.search_owner == auth.user_id):
        selection.delete()
    return "ok"

