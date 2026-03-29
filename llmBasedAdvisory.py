import torch
from transformers import pipeline

# Load model once (important)
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

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
        result = generator(prompt, max_length=100, do_sample=True)

        print("RAW LLM OUTPUT:", result)

        return result[0]['generated_text'].replace(prompt, "").strip()

    except Exception as e:
        print("LLM Error:", e)
        return "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"