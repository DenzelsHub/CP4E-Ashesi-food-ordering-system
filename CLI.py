from food_model import Restaurant, MainDish, Beverage, Snack
from nutrition_lookup import get_nutrition_for_dish
from order_model import Order


def build_sample_restaurants():
    # placeholder data until this gets replaced with real data from the group
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


def show_restaurants(restaurants):
    print("\n=== Restaurants ===")
    names = list(restaurants.keys())
    for i in range(len(names)):
        print(str(i + 1) + ". " + names[i])
    return names


def choose_restaurant(restaurants):
    names = show_restaurants(restaurants)

    while True:
        choice = input("Pick a restaurant (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            chosen_name = names[int(choice) - 1]
            return restaurants[chosen_name]
        print("That's not a valid choice, try again.")


def show_menu(restaurant):
    print("\n=== " + restaurant.get_name() + " ===")
    menu = restaurant.get_menu()
    items = list(menu.values())

    for i in range(len(items)):
        item = items[i]
        nutrition = get_nutrition_for_dish(item.get_name())

        line = str(i + 1) + ". " + item.get_name() + " - GHS " + str(item.get_price())
        line += " (" + item.get_category() + ")"

        if "calories" in nutrition:
            line += " approx " + str(nutrition["calories"]) + " cal"

        print(line)

    return items


def build_cart(restaurant):
    items = show_menu(restaurant)
    cart = []  # list of (item, quantity) tuples

    while True:
        choice = input("\nAdd item number to cart, or 0 to checkout: ")

        if choice == "0":
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
            print("Not a valid item number.")
            continue

        chosen_item = items[int(choice) - 1]
        qty_input = input("Quantity: ")

        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("Enter a valid quantity.")
            continue

        cart.append((chosen_item, int(qty_input)))
        print(chosen_item.get_name() + " added to cart.")

    return cart


def show_cart_summary(cart, restaurant):
    print("\n=== Your Cart ===")
    if len(cart) == 0:
        print("Cart is empty.")
        return

    # placeholder student until Person 1's real student data is wired in
    student = "guest_student"

    order = Order(student, restaurant)
    for item, qty in cart:
        order.add_item(item, qty)
        line_total = item.get_price() * qty
        print(item.get_name() + " x" + str(qty) + " - GHS " + str(line_total))

    total = order.calculate_total()
    print("Total (after any discount): GHS " + str(total))


def main():
    restaurants = build_sample_restaurants()
    restaurant = choose_restaurant(restaurants)
    cart = build_cart(restaurant)
    show_cart_summary(cart, restaurant)


if __name__ == "__main__":
    main()
