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


# Imports for gonnect
#flow_from_clientsecrets creates a flow object from clientsecrets JSON file
#stores client ID and client secretsecret
from oauth2client.client import flow_from_clientsecrets
#used if run into an error exchanging auth. code for access token
from oauth2client.client import FlowExchangeError
import httplib2
import json
#converts return value from function into response object that can be sent to client
from flask import make_response
import requests


#name of running application is argument
#find out more about __name__ in python
#anytime run an app in python __name__ gets run and used for app and all imports used
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Application"


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
    print "the current login session state is: %s" % login_session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print login_session
    print "The current session state is %s" % (login_session['state'])
    return render_template('login.html',  STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Categories).all()
    return render_template('categories.html', categories=categories)

#python decorator
#our function gets wrapped inside the @app.route function
@app.route('/category/<int:category_id>/')
def showCategory(category_id):

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

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Categories(category=request.form['category'], description=request.form['description'])
        session.add(newCategory)
        session.commit()
        flash("new category created!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Categories).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['category']:
            editedCategory.category = request.form['category']
            editedCategory.description = request.form['description']
        session.add(editedCategory)
        session.commit()
        flash("Category was edited")
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category_id=editedCategory.id, category=editedCategory)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Categories).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("Category was deleted")
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html', category_id=categoryToDelete.id, category=categoryToDelete)













@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    #checks to see if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Items(
            item=request.form['item'], category_id=category_id, description=request.form['description'])
        session.add(newItem)
        session.commit()
        flash("new item created!")
        return redirect(url_for('showCategory', category_id=category_id ))
    else:
        return render_template('newitem.html', category_id=category_id)

# Task 2: Create route for editMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    #checks to see if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method== 'POST':
        editedItem = session.query(Items).filter_by(id = category_id).one()
        if request.form['item']:
            editedItem.item = request.form['item']
        session.add(editedItem)
        session.commit()
        flash("Item was edited!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id = item_id)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    #checks to see if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item was deleted")
        return redirect(url_for('showCategory', category_id=category_id))
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
