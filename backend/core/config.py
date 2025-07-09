import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
    NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

settings = Settings()

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

PROMPT = """
Analyze the given food image and identify all distinct food items.

For each item, return:
- "name": the name of the food item (string)
- "confidence": a float between 0 and 1 indicating your confidence level
- "quantity":
    - If the item is countable (like idli, banana), use:
        { "count": <int> }
    - If the item is uncountable (like rice, sambar, chutney), use:
        { "container": "<cup|bowl|glass|large bowl>" }
Use the following reference sizes to estimate quantity more accurately:
- cup: 150 g  
- bowl: 250 g  
- glass: 350 g  
- large bowl: 500 g  

When estimating:
- Count visible discrete items like idlis or pooris.
- Use context to judge how full a bowl or glass is, and choose the closest container name from the list above.
- Always include either "count" or  "container"  for each food item.

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
        "container": "bowl",
      }
    }
  ]
}

Do not include any explanation, description, or markdown — only return pure JSON.
"""