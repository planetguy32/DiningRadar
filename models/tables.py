# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime
from bs4 import BeautifulSoup
import requests
import re
from gluon.scheduler import Scheduler
import time
import exceptions


def get_user_email():
    return auth.user.email if auth.user is not None else None


#More data can be put here
db.define_table('menu_item',
                Field('menu_name'),
                Field('menu_is_eggs', type="boolean"),
                Field('menu_is_fish', type="boolean"),
                Field('menu_is_gluten_free', type="boolean"),
                Field('menu_is_dairy', type="boolean"),
                Field('menu_is_nuts', type="boolean"),
                Field('menu_is_soy', type="boolean"),
                Field('menu_is_vegan', type="boolean"),
                Field('menu_is_vegetarian', type="boolean"),
                Field('menu_is_pork', type="boolean"),
                Field('menu_is_beef', type="boolean"),
                Field('menu_is_halal', type="boolean")
                )

db.define_table('available_food',
                Field('food_id', type="reference menu_item"),
                Field('food_location'),
                Field('food_date', type="integer"),
                Field('food_meal')
                )

db.define_table('saved_searches',
                Field('search_owner', type="reference auth_user"),
                Field('search_url')
                )
