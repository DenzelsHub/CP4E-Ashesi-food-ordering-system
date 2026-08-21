"""
test_nutrition_api.py

Standalone test of the USDA FoodData Central API.
Run this on your own machine (not here) once you have an API key.

Get a free key (no card needed): https://fdc.nal.usda.gov/api-key-signup

Install requests first if you don't have it:
    pip install requests
"""

import requests

API_KEY = 'Kn5el104QquB0RzLdFl8LkrOhCxlJ6MLSCJKyoQk'
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def search_food(query: str, api_key: str = API_KEY):
    """Send one search request and return the raw JSON response."""
    params = {
        "query": query,
        "api_key": api_key,
        "pageSize": 3,  # just get a few results for now
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # crashes loudly if something's wrong -- good for testing
    return response.json()


if __name__ == "__main__":
    # Ghanaian dishes usually won't be found directly -- search by core
    # ingredient instead and treat the result as an approximation.
    test_queries = ["rice", "chicken", "plantain"]


    for query in test_queries:
        print(f"\n--- Searching for: {query} ---")
        data = search_food(query)

        foods = data.get("foods", [])
        if not foods:
            print("No results found.")
            continue

        # just print the first result's key fields so we can see the shape
        first = foods[0]
        print("Description:", first.get("description"))
        print("FDC ID:", first.get("fdcId"))

        nutrients = first.get("foodNutrients", [])
        for n in nutrients[:5]:  # first 5 nutrients only, for now
            print(f"  {n.get('nutrientName')}: {n.get('value')} {n.get('unitName')}")
