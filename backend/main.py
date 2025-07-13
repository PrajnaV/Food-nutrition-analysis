import json
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from Utils.gemini_analyzer import analyze_food_image
from Utils.nutritionix import fetch_nutritionix_data 
from Utils.usda import fetch_food_data, find_best_measure

app = FastAPI()

# CORS middleware: allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Food Image Analysis API."}



@app.post("/get-nutritionix-nutritional-info")
async def get_nutritionix_nutritional_info(file: UploadFile = File(...)):
    response = await analyze_food_image(file)

    if response.status_code != 200:
        return response

    result = json.loads(response.body)
    items = result.get("items", [])
    enriched_items = []

    # Define container capacities (in grams)
    container_capacities = {
        "cup": 150,
        "bowl": 250,
        "glass": 350,
        "large bowl": 500,
        # Add more containers as needed
    }

    for item in items:
        name = item.get("name", "")
        # Capitalize the first letter of the name
        item["name"] = name.capitalize()
        quantity = item.get("quantity", {})

        if "count" in quantity:
            entry = f"{quantity['count']} {name}"
        elif "container" in quantity:
            entry = f"{quantity['container']} {name}"
        else:
            entry = name  # fallback

        # Fetch nutrition data for the entry
        nutrition = await fetch_nutritionix_data(entry)

        # If quantity is defined in terms of container, scale nutrients
        if "container" in quantity:
            container = quantity["container"]
            container_capacity = container_capacities.get(container)
            serving_weight = nutrition.get("serving_weight_grams")
            if container_capacity and serving_weight:
                ratio = container_capacity / serving_weight
                for key in [
                    "nf_calories", "nf_total_fat", "nf_total_carbohydrate", "nf_protein", "nf_sugars"
                ]:
                    if nutrition.get(key) is not None:
                        nutrition[key] = round(nutrition[key] * ratio, 2)
                nutrition["serving_weight_grams"] = round(container_capacity, 2)

        item["nutrition"] = nutrition
        enriched_items.append(item)

    return {"items": enriched_items}


@app.post("/get-usda-nutritional-info")
async def get_usda_nutritional_info(file: UploadFile = File(...)):
    response = await analyze_food_image(file)

    if response.status_code != 200:
        return response

    result = json.loads(response.body)
    items = result.get("items", [])
    description = result.get("description", "")
    enriched_items = []

    # Define container capacities (in grams)
    container_capacities = {
        "cup": 150,
        "bowl": 250,
        "glass": 350,
        "large bowl": 500,
        # Add more containers as needed
    }

    for item in items:
        name = item.get("name", "")
        # Capitalize the first letter of the name
        item["name"] = name.capitalize()
        quantity = item.get("quantity", {})

        # Fetch nutrition data for the entry
        nutrition = await fetch_food_data(name)
        # Proceed only if valid data is returned
        if nutrition.get("error"):
            item["nutrition"] = nutrition
            enriched_items.append(item)
            continue
        if "count" in quantity:
            # If quantity is a count, find best measure
            best_measure = find_best_measure(nutrition.get("foodMeasures", []), name)
            if best_measure:
                nutrition["serving_unit"] = best_measure.get("disseminationText")
                nutrition["serving_weight_grams"] = best_measure.get("gramWeight")
                nutrition["serving_qty"] = quantity["count"]
                nutrition["total_weight_grams"] = nutrition["serving_weight_grams"] * nutrition["serving_qty"]
        elif "container" in quantity:
            # If quantity is a container, use predefined capacity
            container = quantity["container"].lower()
            if container in container_capacities:
                nutrition["serving_unit"] = container
                nutrition["serving_weight_grams"] = container_capacities[container]
                nutrition["serving_qty"] = 1
                nutrition["total_weight_grams"] = nutrition["serving_weight_grams"] * nutrition["serving_qty"]
            else:
                #sort the foodMeasures by rank and use the first one
                best_measure = find_best_measure(nutrition.get("foodMeasures", []), name)
                if best_measure:
                    nutrition["serving_unit"] = best_measure.get("disseminationText")
                    nutrition["serving_weight_grams"] = best_measure.get("gramWeight")
                    nutrition["serving_qty"] = 1
                    nutrition["total_weight_grams"] = nutrition["serving_weight_grams"] * nutrition["serving_qty"]
        #Remove foodMeasures from response
        nutrition.pop("foodMeasures", None)

        # Scale nutrients from per 100g to total_weight_grams
        total_weight = nutrition.get("total_weight_grams")
        if total_weight:
            for key in ["nf_calories", "nf_protein", "nf_total_carbohydrate", "nf_total_fat", "nf_sugars"]:
                if nutrition.get(key) is not None:
                    nutrition[key] = round(nutrition[key] * total_weight / 100, 2)

        item["nutrition"] = nutrition
        enriched_items.append(item)

    return {"items": enriched_items, "description": description}





