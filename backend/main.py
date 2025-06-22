import json
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from Utils.gemini_analyzer import analyze_food_image
from Utils.nutritionix import fetch_nutritionix_data 


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
        elif "container" in quantity:
            entry = f"{quantity['container']} {name}"
        else:
            entry = name  # fallback

        # Fetch nutrition data for the entry
        nutrition = await fetch_nutritionix_data(entry)
        item["nutrition"] = nutrition

        enriched_items.append(item)

    return {"items": enriched_items}





