import os
import json
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from google.generativeai.types import content_types
import mimetypes
import re
import httpx
import requests

load_dotenv(override=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

model = genai.GenerativeModel("models/gemini-1.5-flash")

PROMPT = """
Analyze the given food image and identify all distinct food items.

For each item, return:
- "name": the name of the food item (string)
- "confidence": a float between 0 and 1 indicating your confidence level
- "quantity":
    - If the item is countable (like idli, banana), use:
        { "count": <int> }
    - If the item is uncountable (like rice, curry), use:
        { "container": "<bowl|cup|glass>", "size": "<small|medium|large>" }
- Do not list ingredients separately if they belong to a known, unified dish (e.g., list "burger" not "bun", "patty", etc.)
Return only valid JSON in the following format:

{
  "items": [
    {
      "name": "idli",
      "confidence": 0.92,
      "quantity": {
        "count": 3
      }
    },
    {
      "name": "rice",
      "confidence": 0.88,
      "quantity": {
        "container": "plate",
        "size": "medium"
      }
    }
  ]
}

Do not include any explanation, description, or markdown — only return pure JSON.
"""
@app.get("/")
def root():
    return {"message": "Welcome to the Food Image Analysis API. Use the /analyze endpoint to analyze food images."}



@app.post("/analyze")
async def analyze_food_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file.filename)
        if not mime_type or not mime_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "Invalid image file type."})

        
        # Gemini-compatible image object
        gemini_image = {
            "mime_type": mime_type,
            "data": image_bytes
        }
        # Generate response from Gemini
        response = model.generate_content([PROMPT, gemini_image], stream=False)

        # Extract pure JSON from model response (strip markdown/code fences)
        json_match = re.search(r"\{[\s\S]*\}", response.text)
        if not json_match:
            return JSONResponse(status_code=500, content={"error": "Failed to extract JSON from model response."})

        # Parse and return clean JSON
        parsed = json.loads(json_match.group())
        return JSONResponse(content=parsed)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/print-food-names")
async def print_food_names(file: UploadFile = File(...)):
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




@app.post("/nutritionix-search")
async def fetch_nutritionix_data(query: str):
    try:
        app_id = os.getenv("NUTRITIONIX_APP_ID")
        api_key = os.getenv("NUTRITIONIX_API_KEY")

        if not app_id or not api_key:
            return {"error": "Missing Nutritionix credentials."}

        headers = {
            "x-app-id": app_id,
            "x-app-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = {"query": query}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://trackapi.nutritionix.com/v2/natural/nutrients",
                headers=headers,
                json=body
            )

        if response.status_code != 200:
            return {"error": f"Nutritionix API error: {response.text}"}

        data = response.json()
        food = data.get("foods", [{}])[0]

        return {
            "serving_qty": food.get("serving_qty"),
            "serving_unit": food.get("serving_unit"),
            "serving_weight_grams": food.get("serving_weight_grams"),
            "nf_calories": food.get("nf_calories"),
            "nf_total_fat": food.get("nf_total_fat"),
            "nf_total_carbohydrate": food.get("nf_total_carbohydrate"),
            "nf_protein": food.get("nf_protein")
        }

    except Exception as e:
        return {"error": str(e)}
