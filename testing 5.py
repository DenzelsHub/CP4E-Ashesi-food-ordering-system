
from abc import ABC, abstractmethod


class MenuItem(ABC):
    """Abstract base class for anything sold on a menu."""

    def __init__(self, name: str, price: float, category: str):
        self._name = name
        self._price = price
        self._category = category
        self._nutrition_info = {}  # filled in later by the nutrition API step

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def category(self) -> str:
        return self._category

    @property
    def nutrition_info(self) -> dict:
        return self._nutrition_info

    def set_nutrition_info(self, data: dict) -> None:
        self._nutrition_info = data

    @abstractmethod
    def calculate_price(self) -> float:
        """Subclasses override this -- this is where polymorphism shows up."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self._name} ({self._category}) - GHS {self._price:.2f}"


class MainDish(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, category="Main Dish")

    def calculate_price(self) -> float:
        # placeholder rule: no adjustment for main dishes
        return self._price


class Beverage(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, category="Beverage")

    def calculate_price(self) -> float:
        # placeholder rule: beverages get a flat 10% discount if bought with a main dish
        # (real logic will likely live in Order/discount code -- kept simple here)
        return self._price


class Snack(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, category="Snack")

    def calculate_price(self) -> float:
        return self._price


class Restaurant:
    """Holds a menu of MenuItem objects, keyed by item name."""

    def __init__(self, name: str):
        self._name = name
        self._menu: dict[str, MenuItem] = {}
        self._popular_items: set[str] = set()

    @property
    def name(self) -> str:
        return self._name

    def add_item(self, item: MenuItem) -> None:
        self._menu[item.name] = item

    def get_menu(self) -> dict:
        return self._menu

    def mark_popular(self, item_name: str) -> None:
        if item_name in self._menu:
            self._popular_items.add(item_name)

    def get_popular_items(self) -> set:
        return self._popular_items


def build_sample_restaurants() -> dict:
    """
    Returns a dict of {restaurant_name: Restaurant} pre-loaded with common
    Ghanaian dishes and placeholder prices (GHS). Replace/adjust prices as
    needed once you have real menu data.
    """
    restaurants = {}

    akornor = Restaurant("Akornor Kitchen")
    akornor.add_item(MainDish("Jollof Rice", 15.00))
    akornor.add_item(MainDish("Waakye", 30.00))
    akornor.add_item(MainDish("Banku and Tilapia", 35.00))
    akornor.add_item(MainDish("Fufu and Light Soup", 30.00))
    akornor.add_item(Beverage("Sobolo", 8.00))
    akornor.add_item(Beverage("Water", 3.00))
    akornor.add_item(Snack("Meat Pie", 6.00))
    akornor.mark_popular("Waakye")
    restaurants[akornor.name] = akornor

    Hallmark_cafe = Restaurant("Ashesi Cafeteria")
    Hallmark_cafe.add_item(MainDish("Red Red", 22.00))
    Hallmark_cafe.add_item(MainDish("Kenkey and Fish", 28.00))
    Hallmark_cafe.add_item(MainDish("Fried Rice and Chicken", 30.00))
    Hallmark_cafe.add_item(Beverage("Bissap", 8.00))
    Hallmark_cafe.add_item(Beverage("Malt", 10.00))
    Hallmark_cafe.add_item(Snack("Kelewele", 10.00))
    Hallmark_cafe.add_item(Snack("Chin Chin", 5.00))
    Hallmark_cafe.mark_popular("Red Red")
    restaurants[ Hallmark_cafe.name] = Hallmark_cafe

    Munchies = Restaurant("Munchies")
    Munchies.add_item(MainDish("Fufu", 24.00))
    Munchies.add_item(MainDish("Rice Balls and Groundnut Soup", 27.00))
    Munchies.add_item(Beverage("Zobo", 7.00))
    Munchies.add_item(Snack("kelewele", 24.00))
    Munchies.add_item(Snack("waffles", 18.00))
    restaurants[  Munchies.name] =   Munchies

    return restaurants


if __name__ == "__main__":
    # quick manual test -- run this file directly to see it work
    restaurants = build_sample_restaurants()

    for r_name, restaurant in restaurants.items():
        print(f"\n=== {r_name} ===")
        for item in restaurant.get_menu().values():
            print(" -", item)
        if restaurant.get_popular_items():
            print("Popular:", ", ".join(restaurant.get_popular_items()))
