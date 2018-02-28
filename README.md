# Item Catalog

## About

This is the fourth project in the Full Stack Web Developer Nanodegree program from Udacity. The project is a web application item catalog allowing authenticated users to perform CRUD operations within a relational database. A google+ OAuth 2.0 sign in is used to authenticate users. Authenticated Users can create, update and delete items from the catalog using a local permissioin system allowing only users that created an item or category to edit or delete that item. JSON endpoints are provided for all items in the database with their respective HTTP links.

The app is built with the Flask web framework and uses a SQLite database. The webpages are styled with the bootstrap CSS framework.

## Requirements

* Python 2


## Installation Instructions

1. install virtualenv
`sudo pip install virtualenv`

article explaining virtualenv and its importance: https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/


2. clone this repository
`git clone https://github.com/dylance/Udacity-FSND-Project4`

3. change directory into git repo
`cd Udacity-FSND-Project4`

4. create local virtualenv environment
`virtualenv venv`

5. activate virtualenv environment
`source venv/bin/activate`

6. install dependencies
`pip install --editable .`

7. change directory into item_catalog
`cd item_catalog`

8. set up db
`python database_setup.py`

9. add default categories to database (optional)
`python add_categories.py`

10. run server
`python server.py`

11. view server in browser localhost:8000/

## Creator
Dylan Ellison
