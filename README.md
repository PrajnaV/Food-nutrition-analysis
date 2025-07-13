# Food Nutrition Analysis Backend

This backend is a FastAPI application for food image analysis and nutrition information retrieval. It uses Google Gemini for food recognition and can fetch nutrition data from both Nutritionix and USDA databases. You can analyze food images and get detailed nutrition info for each item, including calories, protein, fat, carbohydrates, and sugars.

## Features

- Analyze food images to identify food items using Gemini AI
- Retrieve nutritional information for identified foods using Nutritionix or USDA
- Modular code structure for easy maintenance and extension

## Prerequisites

- Python 3.12+
- [Nutritionix API credentials](https://developer.nutritionix.com/)
- [Google Gemini API key](https://ai.google.dev/)
- [USDA API key](https://fdc.nal.usda.gov/api-key-signup.html)

## Setup Instructions

1. **Clone the repository**

```sh
git clone https://github.com/PrajnaV/Food-nutrition-analysis.git
cd Food-nutrition-analysis/backend
```

2. **Create and activate a virtual environment**

On Windows PowerShell:

```sh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**

```sh
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the `backend` directory with the following content:

```
GOOGLE_API_KEY=your_google_gemini_api_key
NUTRITIONIX_APP_ID=your_nutritionix_app_id
NUTRITIONIX_API_KEY=your_nutritionix_api_key
USDA_API_KEY=your_usda_api_key
```

5. **Run the FastAPI application**

```sh
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints

- `GET /` — Welcome message
- `POST /get-nutritionix-nutritional-info/` — Analyze a food image and return items with Nutritionix nutrition info
- `POST /get-usda-nutritional-info/` — Analyze a food image and return items with USDA nutrition info

## Example Usage

You can use Swagger UI to test the API:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Upload a food image to `/get-nutritionix-nutritional-info/` for Nutritionix data or `/get-usda-nutritional-info/` for USDA data.

---

**Note:** Ensure your API keys are valid and you have internet access for the AI and nutrition APIs.
