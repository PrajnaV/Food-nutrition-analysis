import os
import json
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from google.generativeai.types import content_types
import mimetypes
import re

load_dotenv()

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
