import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

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

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()

    try:
        return result[0]["generated_text"]
    except Exception:
        return "मौसम सामान्य है, नियमित सिंचाई करें।"