import mimetypes
import re
import json
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from core.config import model, PROMPT

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