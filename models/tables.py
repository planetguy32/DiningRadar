# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None


#More data can be put here
db.define_table('menu_item',
                Field('name')
                )

db.define_table('available_food',
                Field('food_id', type="reference menu_item"),
                Field('location'),
                Field('date')
                )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
