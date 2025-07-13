import os
import httpx
from dotenv import load_dotenv
import re

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"



async def fetch_food_data(name: str):
    """
    Fetch nutrition data for a food item from the USDA FoodData Central API.
    Extracts and returns only energy, protein, carbohydrate, fat, and foodMeasures.
    
    Args:
        name (str): Name of the food item to search for.

    Returns:
        dict: Nutrition data result from USDA API, or error message.
    """
    params = {
        "api_key": USDA_API_KEY,
        "query": name,
        "pageSize": 5,
        "dataType": "Survey (FNDDS)"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(USDA_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        foods = data.get("foods", [])
        
        if foods:
            food = foods[0]
            nutrients = food.get("foodNutrients", [])
            # Map USDA nutrient names to Nutritionix keys
            nutrient_map = {
                "Energy": "nf_calories",
                "Protein": "nf_protein",
                "Carbohydrate, by difference": "nf_total_carbohydrate",
                "Total lipid (fat)": "nf_total_fat",
                "Sugars, total including NLEA": "nf_sugars"
            }
            result = {}
            for n in nutrients:
                name = n.get("nutrientName")
                if name in nutrient_map:
                    result[nutrient_map[name]] = n.get("value")
            result["foodMeasures"] = food.get("foodMeasures", [])
            return result
        return {"error": "Food data not found in USDA database."}

    except httpx.RequestError as e:
        return {"error": f"USDA API error: {str(e)}"}
    


def find_best_measure(food_measures, food_name):
    # Sort by rank (lower = better)
    sorted_measures = sorted(food_measures, key=lambda x: x['rank'])
    
    # Create priority patterns for matching
    priority_patterns = [
        r"1\s+(whole|item|piece|serving)",  # Highest priority - generic whole items
        r"1\s+" + re.escape(food_name.lower()),  # "1 tomato"
        r"1\s+\w+\s+" + re.escape(food_name.lower()),  # "1 plum tomato"
        r"1\s+[^\s]+",  # Any other "1 something" pattern
    ]
    
    # Try each priority level
    for pattern in priority_patterns:
        for measure in sorted_measures:
            if re.search(pattern, measure['disseminationText'].lower()):
                return measure
                
    # Fallback to first ranked measure if no matches
    return sorted_measures[0]