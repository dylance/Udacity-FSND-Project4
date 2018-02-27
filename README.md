# Udacity Full STack Web Developer Item Catalog

## About

This is the fourth project in Udacity Full Stack Web Developer Nanodegree. The project is an item catalog application that lets logged in users create cateogries and items for those categories. The program uses a Flask Server and sqlite databse to perform CRUD operations on data for the Item Catalog. The websites are built using the bootstrap framework.

## Requirements

Python 2


## Installation Instructions


1. install virtualenv
`sudo pip install virtualenv`

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

7. change directory into course_catalog
`cd course_catalog`

8. set up db
`python database_setup.py`

9. add default categories to database (optional)
`python add_categories.py`

10. run server
`python server.py`

11. view server in browser localhost:5000/






old instructions that I don't want to delete just yet

install Vagrant VM
install git
install virtual box - https://www.virtualbox.org/wiki/Downloads - only the platform package is required. no need to launch after installation

install vagrant https://www.vagrantup.com/downloads.html

fork this repo https://github.com/udacity/OAuth2.0

change direcoty into oath and run vagrant up

type vagrant ssh

cd /vagrant
