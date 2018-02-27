# Udacity Full STack Web Developer Item Catalog

## About

This is the fourth project in Udacity Full Stack Web Developer Nanodegree. The project is an item catalog application that lets logged in users create cateogries and items for those categories. The program uses a Flask Server and sqlite databse to perform CRUD operations on data for the Item Catalog. The webpages are built using the bootstrap framework.

## Requirements

Python 2


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

11. view server in browser localhost:5000/
