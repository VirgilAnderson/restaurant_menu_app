from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Routes
# Show All Restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "This page will show all my restaurants"

# Create New Restaurant
@app.route('/restaurants/new')
def newRestaurant():
    return "This page will let me create a new restaurant"

# Edit Restaurants
@app.route('/restaurants/restaurant_id/edit')
def editRestaurant():
    return "This page will let me edit %s"

# Delete Restaurants
@app.route('/restaurants/restaurant_id/delete')
def deleteRestaurant():
    return "This page will let me delete %s"

# Show Menu
@app.route('/restaurants/restaurant_id/')
@app.route('/restaurants/restaurant_id/menu')
def showMenu():
    return "This page will show the menu for %s"

# Create Menu item
@app.route('/restaurants/restaurant_id/menu/new')
def newMenu():
    return "This page will let me create a new menu item"

# Edit Menu items
@app.route('/restaurants/restaurant_id/menu/menu_id/edit')
def editMenu():
    return "This page will let me edit menu item %s"

# Delete Menu
@app.route('/restaurants/restaurant_id/menu_id/delete')
def deleteMenuItem():
    return "This page will let me delete menu item %s"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5001)
