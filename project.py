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
    #return "This page will show all my restaurants"
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# Create New Restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    #return "This page will let me create a new restaurant"
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('showMenu', restaurant_id = newRestaurant.id))
    else:
        return render_template('newRestaurant.html')

# Edit Restaurants
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # This page will let me edit restaurants
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Edited")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant = editedRestaurant)

# Delete Restaurants
@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # This page will let me delete restaurants
    deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        flash("Restaurant Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = deleteRestaurant)

# Show Menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # Read all the menu items for the restaurant
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()

    # Query Appetizers
    appetizers = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Appetizer').all()
    # check if empty
    appetizersFlag = ''
    if not appetizers:
        appetizersFlag = 'display:none;'

    # Query salad
    salad = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Salad').all()
    # check if empty
    saladFlag = ''
    if not salad:
        saladFlag = 'display:none;'

    # Query soup
    soup = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Soup').all()
    soupFlag = ''
    if not soup:
        soupFlag = 'display:none;'

    # Query Fish
    fish = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Fish').all()
    # Check if empty
    fishFlag = ''
    if not fish:
        fishFlag = 'display:none;'

    # Query Entree
    entree = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Entree').all()
    # Check if empty
    entreeFlag = ''
    if not entree:
        entreeFlag = 'display:none;'

    # Query Dessert
    dessert = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Dessert').all()
    # check if empty
    dessertFlag = ''
    if not dessert:
        dessertFlag = 'display:none;'

    # Query Drinks
    drinks = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, course = 'Drinks').all()
    # check if empty
    drinksFlag = ''
    if not drinks:
        drinksFlag = 'display:none;'

    return render_template('menu.html', restaurant = restaurant, menuItems = items, appetizers = appetizers, salad = salad, soup = soup, fish = fish, entree = entree, dessert = dessert, drinks = drinks, appetizersFlag = appetizersFlag, saladFlag = saladFlag, soupFlag = soupFlag, fishFlag = fishFlag, entreeFlag = entreeFlag, dessertFlag = dessertFlag, drinksFlag = drinksFlag)

# Create Menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # Add a new menu item for the restaurant
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], price = request.form['price'], course = request.form['course'], description = request.form['description'], restaurant_id = restaurant.id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for('showMenu', restaurant_id = restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant = restaurant)

# Edit Menu items
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # Edit a menu item for the restaurant
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Updated")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

# Delete Menu Item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # Delete a menu item from restaurant
    deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu Item Deleted")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = deleteItem)

# Menu API Endpoint
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

# Restaurant API Endpoint
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5001)
