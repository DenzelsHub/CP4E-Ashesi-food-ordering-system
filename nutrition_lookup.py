import requests

# Get your key here: https://fdc.nal.usda.gov/api-key-signup
API_KEY = "Kn5el104QquB0RzLdFl8LkrOhCxlJ6MLSCJKyoQk"
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# USDA doesn't have Ghanaian dish names, so we map each dish to a
# basic ingredient we can actually search for. The result is just
# an approximation, not the exact dish.
ingredient_map = {
    "Jollof Rice": "rice",
    "Waakye": "rice and beans",
    "Banku and Tilapia": "tilapia",
    "Fufu and Light Soup": "cassava",
    "Red Red": "beans",
    "Kenkey and Fish": "fish",
    "Fried Rice and Chicken": "chicken",
    "Yam and Palava Sauce": "yam",
    "Rice Balls and Groundnut Soup": "peanut",
    "Sobolo": "hibiscus tea",
    "Water": "water",
    "Bissap": "hibiscus tea",
    "Malt": "malt beverage",
    "Zobo": "hibiscus tea",
    "Meat Pie": "meat pie",
    "Kelewele": "plantain",
    "Chin Chin": "fried dough",
    "Spring Rolls": "spring roll",
    "Plantain Chips": "plantain chips",
}

# only care about these 4 nutrients out of the many USDA returns
nutrients_we_want = {
    "Energy": "calories",
    "Protein": "protein_g",
    "Total lipid (fat)": "fat_g",
    "Carbohydrate, by difference": "carbs_g",
}

# cache so we don't call the API again for a dish we already looked up
nutrition_cache = {}


def get_nutrition_for_dish(dish_name):
    # check cache first
    if dish_name in nutrition_cache:
        return nutrition_cache[dish_name]

    # figure out what to actually search for
    if dish_name in ingredient_map:
        query = ingredient_map[dish_name]
    else:
        query = dish_name

    params = {
        "query": query,
        "api_key": API_KEY,
        "pageSize": 1
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("API request failed for", dish_name, "-", e)
        return {}

    foods = data.get("foods", [])
    if len(foods) == 0:
        print("No match found for", dish_name, "(searched:", query, ")")
        return {}

    first_food = foods[0]
    food_nutrients = first_food.get("foodNutrients", [])

    # pull out just the 4 nutrients we care about
    result = {}
    for nutrient in food_nutrients:
        name = nutrient.get("nutrientName")
        if name in nutrients_we_want:
            short_name = nutrients_we_want[name]
            result[short_name] = nutrient.get("value")

    result["source"] = first_food.get("description")

    nutrition_cache[dish_name] = result
    return result


if __name__ == "__main__":
    test_dishes = ["Jollof Rice", "Waakye", "Kelewele"]

    for dish in test_dishes:
        print("\n---", dish, "---")
        info = get_nutrition_for_dish(dish)
        if len(info) == 0:
            print("  No data found.")
        else:
            for key in info:
                print(" ", key, ":", info[key])
