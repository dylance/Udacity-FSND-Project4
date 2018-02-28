# Item Catalog

## About

This is the fourth project in the Full Stack Web Developer Nanodegree from Udacity. The project is an item catalog application which uses a google+ OAuth 2.0 sign in to authenticate users. Authenticated Users can create, update and delete items from the catalog. The application uses a local permission system allowing only users that created an item or category to edit the category or item. The app uses the Flask web framework and SQLite database. The webpages are built styled the bootstrap CSS framework.

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
