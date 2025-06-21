import os
import httpx

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
