from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items


#name of running application is argument
#find out more about __name__ in python
#anytime run an app in python __name__ gets run and used for app and all imports used
app = Flask(__name__)

APPLICATION_NAME = "Item Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///project2nd.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#python decorator
#our function gets wrapped inside the @app.route function
@app.route('/')
@app.route('/category/<int:category_id>/')
def showCategories(category_id):

    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=category.id)
    return render_template('category_items.html', category=category, items=items)

    #look up query method for sql alchemy. dbSession.query
    #query to view items from category with custom url
    """category1 = session.query(Categories).first()
    items = session.query(Items).filter_by(category_id=category1.id)
    output = ''
    for i in items:
        output += i.item
        output += " - "
        output += i.description
        output += '</br></br>'
    return output"""
#test function I made to print out all categories
@app.route('/test')
def showCategories2():
    #look up query method for sql alchemy. dbSession.query
    category1 = session.query(Categories).all()

    output = ''
    for i in category1:
        output += i.category
        output += '</br>'
    return output

# Task 1: Create route for newMenuItem function here

@app.route('/category/<int:category_id>/add/')
def newItem(category_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
    return "page to edit a item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
    return "page to delete a menu item. Task 3 complete!"



#the app run by python interpreter gets a variable set to __main__
#imported python code gets named __<file name>__
if __name__ == '__main__':
    #allows server to reload itself each time it notices a code change
    #provides debugger in browser also
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
