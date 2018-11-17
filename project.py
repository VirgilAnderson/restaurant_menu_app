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
    restaurants = session.query(Restaurant).all();
    return render_template('restaurants.html', restaurants = restaurants)

# Create New Restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    #return "This page will let me create a new restaurant"
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
    else:
        return render_template('newRestaurant.html')

# Edit Restaurants
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    #return "This page will let me edit %s"
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant = editedRestaurant)

# Delete Restaurants
@app.route('/restaurants/restaurant_id/delete')
def deleteRestaurant():
    #return "This page will let me delete %s"
    return render_template('deleteRestaurant.html', restaurant = restaurant)

# Show Menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    #return "This page will show the menu for %s"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('menu.html', restaurant = restaurant, menuItems = items)

# Create Menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    #return "This page will let me create a new menu item"
    return render_template('newMenuItem.html', restaurant = restaurant_id)

# Edit Menu items
@app.route('/restaurants/restaurant_id/menu/menu_id/edit')
def editMenuItem():
    #return "This page will let me edit menu item %s"
    return render_template('editMenuItem.html', restaurant = restaurant, item = item)

# Delete Menu
@app.route('/restaurants/restaurant_id/menu_id/delete')
def deleteMenuItem():
    #return "This page will let me delete menu item %s"

    return render_template('deleteMenuItem.html', restaurant = restaurant, item = item)

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5001)
