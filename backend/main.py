import json
from fastapi import FastAPI, File, UploadFile
from Utils.gemini_analyzer import analyze_food_image
from Utils.nutritionix import fetch_nutritionix_data 


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Food Image Analysis API."}



@app.post("/get-nutritional-info")
async def get_nutritional_info(file: UploadFile = File(...)):
    response = await analyze_food_image(file)

    if response.status_code != 200:
        return response

    result = json.loads(response.body)
    items = result.get("items", [])
    enriched_items = []

    for item in items:
        name = item.get("name", "")
        quantity = item.get("quantity", {})

        if "count" in quantity:
            entry = f"{quantity['count']} {name}"
        elif "container" in quantity and "size" in quantity:
            entry = f"{quantity['size']} {quantity['container']} {name}"
        else:
            entry = name  # fallback

        # Fetch nutrition data for the entry
        nutrition = await fetch_nutritionix_data(entry)
        item["nutrition"] = nutrition

        enriched_items.append(item)

    return {"items": enriched_items}





