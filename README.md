# Food Nutrition Analysis Backend

This backend is a FastAPI application for food image analysis and nutrition information retrieval. It uses Google Gemini for food recognition and the Nutritionix API for nutritional data.

## Features
- Analyze food images to identify food items using Gemini AI
- Retrieve nutritional information for identified foods using Nutritionix
- Modular code structure for easy maintenance and extension

## Prerequisites
- Python 3.12+
- [Nutritionix API credentials](https://developer.nutritionix.com/)
- [Google Gemini API key](https://ai.google.dev/)

## Setup Instructions

1. **Clone the repository**

```sh
git clone <your-repo-url>
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
```

5. **Run the FastAPI application**

```sh
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints

- `GET /` — Welcome message
- `POST /get-nutritional-info/` — Analyze a food image and return items with nutrition info

## Example Usage

You can use Swagger UI to test the API:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



---

**Note:** Ensure your API keys are valid and you have internet access for the AI and nutrition APIs.
