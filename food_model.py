from abc import ABC, abstractmethod


class MenuItem(ABC):
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    @abstractmethod
    def get_category(self):
        pass

    def __str__(self):
        return self.__name + " - GHS " + str(self.__price) + " (" + self.get_category() + ")"


class MainDish(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def get_category(self):
        return "Main Dish"


class Beverage(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def get_category(self):
        return "Beverage"


class Snack(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def get_category(self):
        return "Snack"


class Restaurant:
    def __init__(self, name, location):
        self.__name = name
        self.__location = location
        self.__menu = {}
        self.__popular_items = set()

    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def add_item(self, item):
        self.__menu[item.get_name()] = item

    def mark_popular(self, item_name):
        if item_name in self.__menu:
            self.__popular_items.add(item_name)

    def get_menu(self):
        return self.__menu

    def get_popular_items(self):
        return self.__popular_items

    def display_menu(self):
        print("Menu for " + self.__name + " at " + self.__location)
        for item in self.__menu.values():
            print(item)


class Student:
    def __init__(self, name, student_id, email):
        self.__name = name
        self.__student_id = student_id
        self.__email = email

    def get_name(self):
        return self.__name

    def get_student_id(self):
        return self.__student_id

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def __str__(self):
        return "Name: " + self.__name + ", ID: " + self.__student_id



