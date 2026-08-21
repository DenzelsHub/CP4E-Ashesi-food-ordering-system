from flask import Flask, render_template, request, redirect, session

from food_model import Restaurant, MainDish, Beverage, Snack
from nutrition_lookup import get_nutrition_for_dish
from order_model import Order

app = Flask(__name__)
app.secret_key = "change_this_later"  # needed for session to work


def build_sample_restaurants():
    restaurants = {}

    akornor = Restaurant("Akornor Kitchen", "Ashesi Campus")
    akornor.add_item(MainDish("Jollof Rice", 25.00))
    akornor.add_item(MainDish("Waakye", 20.00))
    akornor.add_item(Beverage("Water", 3.00))
    akornor.add_item(Snack("Meat Pie", 6.00))
    restaurants[akornor.get_name()] = akornor

    cafeteria = Restaurant("Ashesi Cafeteria", "Main Campus")
    cafeteria.add_item(MainDish("Red Red", 22.00))
    cafeteria.add_item(MainDish("Kenkey and Fish", 28.00))
    cafeteria.add_item(Beverage("Bissap", 8.00))
    cafeteria.add_item(Snack("Kelewele", 10.00))
    restaurants[cafeteria.get_name()] = cafeteria

    return restaurants


# built once when the app starts, shared across everyone visiting the site
all_restaurants = build_sample_restaurants()


@app.route("/")
def home():
    return render_template("index.html", restaurants=all_restaurants)


@app.route("/menu/<restaurant_name>")
def menu(restaurant_name):
    restaurant = all_restaurants[restaurant_name]
    items = restaurant.get_menu()

    # attach nutrition info to each item for the template to use
    menu_data = []
    for item in items.values():
        nutrition = get_nutrition_for_dish(item.get_name())
        menu_data.append({
            "name": item.get_name(),
            "price": item.get_price(),
            "category": item.get_category(),
            "calories": nutrition.get("calories")
        })

    # remember which restaurant this session is ordering from
    session["restaurant_name"] = restaurant_name

    return render_template("menu.html", restaurant=restaurant, menu_data=menu_data)


@app.route("/add", methods=["POST"])
def add_to_cart():
    item_name = request.form["item_name"]
    quantity = int(request.form["quantity"])

    # cart lives in the session as a plain list of dicts (can't store
    # MenuItem objects directly in a session, so we just keep the name)
    cart = session.get("cart", [])
    cart.append({"item_name": item_name, "quantity": quantity})
    session["cart"] = cart

    restaurant_name = session["restaurant_name"]
    return redirect("/menu/" + restaurant_name)


@app.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    restaurant_name = session.get("restaurant_name")

    if not restaurant_name or len(cart) == 0:
        return render_template("cart.html", cart_lines=[], total=0)

    restaurant = all_restaurants[restaurant_name]
    menu = restaurant.get_menu()

    # rebuild an Order object using the real MenuItem objects
    order = Order("guest_student", restaurant)
    cart_lines = []

    for entry in cart:
        item = menu[entry["item_name"]]
        quantity = entry["quantity"]
        order.add_item(item, quantity)

        line_total = item.get_price() * quantity
        cart_lines.append({
            "name": item.get_name(),
            "quantity": quantity,
            "line_total": line_total
        })

    total = order.calculate_total()
    return render_template("cart.html", cart_lines=cart_lines, total=total)


@app.route("/checkout", methods=["POST"])
def checkout():
    # clear the cart after "placing the order"
    session["cart"] = []
    return render_template("receipt.html")


if __name__ == "__main__":
    app.run(debug=True)
