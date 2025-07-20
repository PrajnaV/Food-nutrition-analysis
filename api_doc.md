# Food Nutrition Analysis API Documentation

This document describes the available API endpoints for the Food Nutrition Analysis backend. These endpoints allow you to analyze food images and retrieve nutrition information using either Nutritionix or USDA databases.

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Analyze Food Image and Get Nutritionix Nutrition Info

**POST** `/get-nutritionix-nutritional-info/`

- **Description:**
  Analyze a food image and return a list of detected food items with nutrition information from Nutritionix.

- **Request:**

  - Content-Type: `multipart/form-data`
  - Body: `file` (image file, required)

- **Response:**
  - 200 OK
  - JSON:
    ```json
    {
    "items": [
        {
        "name": "Samosa",
        "confidence": 0.95,
        "quantity": {
            "count": 5
        },
        "nutrition": {
            "serving_qty": 5,
            "serving_unit": "samosa",
            "serving_weight_grams": 500,
            "nf_calories": 1307.49,
            "nf_total_fat": 86.21,
            "nf_total_carbohydrate": 119.53,
            "nf_protein": 17.43,
            "nf_sugars": 7.96
        }
        },
        {
        "name": "Green chutney",
        "confidence": 0.9,
        "quantity": {
            "container": "bowl"
        },
        "nutrition": {
            "serving_qty": 1,
            "serving_unit": "bowl",
            "serving_weight_grams": 250,
            "nf_calories": 304,
            "nf_total_fat": 20.76,
            "nf_total_carbohydrate": 24.57,
            "nf_protein": 12.51,
            "nf_sugars": 6.53
        }
        }
    ],
    "description": "Five samosas served with a bowl of green chutney."
    }
    }
    ```

---

### 2. Analyze Food Image and Get USDA Nutrition Info

**POST** `/get-usda-nutritional-info/`

- **Description:**
  Analyze a food image and return a list of detected food items with nutrition information from the USDA database.

- **Request:**

  - Content-Type: `multipart/form-data`
  - Body: `file` (image file, required)

- **Response:**
  - 200 OK
  - JSON:
    ```json
    {
    "items": [
        {
        "name": "Idli",
        "confidence": 0.95,
        "quantity": {
            "count": 4
        },
        "nutrition": {
            "nf_protein": 9.67,
            "nf_total_fat": 0.53,
            "nf_total_carbohydrate": 37.97,
            "nf_calories": 194.56,
            "serving_unit": "1 item",
            "serving_weight_grams": 38,
            "serving_qty": 4,
            "total_weight_grams": 152
        }
        },
        {
        "name": "Sambar",
        "confidence": 0.9,
        "quantity": {
            "container": "bowl"
        },
        "nutrition": {
            "nf_protein": 10.82,
            "nf_total_fat": 6.78,
            "nf_total_carbohydrate": 29.43,
            "nf_calories": 215,
            "serving_unit": "bowl",
            "serving_weight_grams": 250,
            "serving_qty": 1,
            "total_weight_grams": 250
        }
        },
        {
        "name": "Red chutney",
        "confidence": 0.85,
        "quantity": {
            "container": "cup"
        },
        "nutrition": {
            "nf_protein": 0.49,
            "nf_total_fat": 0.09,
            "nf_total_carbohydrate": 90.9,
            "nf_calories": 369,
            "serving_unit": "cup",
            "serving_weight_grams": 150,
            "serving_qty": 1,
            "total_weight_grams": 150
        }
        },
        {
        "name": "Green chutney",
        "confidence": 0.85,
        "quantity": {
            "container": "cup"
        },
        "nutrition": {
            "nf_protein": 0.49,
            "nf_total_fat": 0.09,
            "nf_total_carbohydrate": 90.9,
            "nf_calories": 369,
            "serving_unit": "cup",
            "serving_weight_grams": 150,
            "serving_qty": 1,
            "total_weight_grams": 150
        }
        }
    ],
    "description": "A plate of 4 idlis served with a bowl of sambar, a cup of red chutney, and a cup of green chutney."
    }
    ```

---

## Error Handling

- If an error occurs (e.g., missing API key, invalid image), the response will include an `error` field with a message.

---

