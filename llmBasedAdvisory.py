import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Use lighter & more stable model
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def generate_advisory(risks, weather):
    prompt = f"""
You are a Krishi expert helping Indian farmers.

Convert this risk data into actionable advice.

Weather:
Temp: {weather['temperature']}°C
Humidity: {weather['humidity']}%
Rainfall: {weather['rainfall']} mm
Wind-Speed: {weather['wind_speed']} m/s

Risks:
{risks}

Rules:
- Use simple Hindi
- Give 2–3 short suggestions
- Focus on crops

Answer:
"""

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=15
        )

        # Debug logs (VERY IMPORTANT)
        print("STATUS:", response.status_code)
        print("TEXT RESPONSE:", response.text)

    except Exception as e:
        print("Request Error:", e)
        return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"

    # Try parsing JSON safely
    try:
        result = response.json()
    except Exception:
        print("JSON Parse Error")
        print("RAW TEXT:", response.text)
        return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"

    print("PARSED RESPONSE:", result)

    # Handle different response formats
    try:
        if isinstance(result, list):
            return result[0]["generated_text"]

        elif isinstance(result, dict):
            if "generated_text" in result:
                return result["generated_text"]

            elif "error" in result:
                print("HF API Error:", result["error"])
                return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"

        print("Unexpected format:", result)
        return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"

    except Exception as e:
        print("Parsing Error:", e)
        return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"