from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

#imports for creating log in
# session is renamed login_session because we already have an instance of session
#session works like a dictionary to store values for as long as a session with a server exists
from flask import session as login_session
import random
import string
#name of running application is argument
#find out more about __name__ in python
#anytime run an app in python __name__ gets run and used for app and all imports used
app = Flask(__name__)

APPLICATION_NAME = "Item Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///project3rd.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token to ensure the the actual user is making requests
# Used to make sure user and login sessions have same state variable
# when a user tries to authenticate
@app.route('/login')
def showLogin():
    print "the current login session sate is: %s" % login_session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print login_session
    return "The current session state is %s" % login_session['state']


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


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Items(
            item=request.form['item'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("new item created!")
        return redirect(url_for('showCategories', category_id=category_id ))
    else:
        return render_template('newitem.html', category_id=category_id)

# Task 2: Create route for editMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Items).filter_by(id = item_id).one()
    if request.method== 'POST':
        if request.form['item']:
            editedItem.item = request.form['item']
        session.add(editedItem)
        session.commit()
        flash("Item was edited!")
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id = item_id, item = editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item was deleted")
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteitem.html', category_id=category_id,item=itemToDelete)



#JSON endpoints
@app.route('/category/<int:category_id>/JSON')
def restaurantMenuJSON(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(
        category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def menuItemJSON(category_id, item_id):
    item = session.query(Items).filter_by(id=item_id).one()
    return jsonify(Items=item.serialize)




#the app run by python interpreter gets a variable set to __main__
#imported python code gets named __<file name>__
if __name__ == '__main__':
    app.secret_key = 'secretkey'
    #allows server to reload itself each time it notices a code change
    #provides debugger in browser also
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
