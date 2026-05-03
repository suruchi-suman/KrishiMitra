from dotenv import load_dotenv
import os
import re
from flask_cors import CORS

 
load_dotenv()

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = "gemini-2.5-flash"

import requests
from flask import Flask, request, jsonify
import json
from flask import Response

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

API_KEY = os.getenv("WEATHER_API_KEY")

# FETCH WEATHER DATA FUNCTION
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "मौसम डेटा प्राप्त करने में त्रुटि")}

        weather_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["main"]
        }

        return weather_data

    except Exception as e:
        return {"error": str(e)}


# 2. LOADING ML MODEL TO PREDICT RISKS
import joblib

risk_model = joblib.load("risk_model.pkl")


# 3. PREDICTION FUNCTION
def predict_risks(temp, humidity, rainfall, wind):
    input_data = [[temp, humidity, rainfall, wind]]
    pred = risk_model.predict(input_data)[0]

    labels = ["heat_stress", "low_moisture", "flood_risk", "fungal_risk", "cold_stress"]

    return [labels[i] for i in range(len(labels)) if pred[i] == 1]


# def fallback_advisory(risks, weather):
#     if "low_moisture" in risks:
#         return "मिट्टी में नमी कम है, सिंचाई बढ़ाएं और मल्चिंग करें।"
#     if "heat_stress" in risks:
#         return "उच्च तापमान है, फसल को धूप से बचाएं और सिंचाई करें।"
#     if "fungal_risk" in risks:
#         return "आर्द्रता अधिक है, फफूंद से बचाव के लिए दवा का छिड़काव करें।"
#     return "मौसम सामान्य है, नियमित देखभाल करें।"


def generate_advisory(risks, weather):
    try:
        # Handle no risk case
        if not risks:
            return "मौसम सामान्य है, फसल की नियमित देखभाल करें।"

        risks_text = ", ".join(risks)

        prompt = f"""
आप एक अनुभवी कृषि विशेषज्ञ हैं।

मौसम:
तापमान: {weather['temperature']}°C
आर्द्रता: {weather['humidity']}%
हवा की गति: {weather['wind_speed']} m/s

जोखिम:
{risks_text}

निर्देश:
- 2-3 छोटे और स्पष्ट सुझाव दें
- सरल हिंदी में लिखें
- किसान को सीधे सलाह दें

उत्तर:
"""

        response = client.models.generate_content(
            model=gemini_model,
            contents=prompt
        )

        output = response.text.strip()
        output = re.sub(r"\*\*(.*?)\*\*", r"\1", output)
        output = output.replace("\n", "<br>")
        output = re.sub(r"\s+", " ", output).strip()

        if not output:
            raise ValueError("Empty Gemini response")

        return output

    except Exception as e:
        print("Gemini Error:", e)
        return f"LLM Error: {str(e)}"
        # return fallback_advisory(risks, weather)


# 5. GET WEATHER ADVISORY
def get_weather_advisory(city):
    weather = get_weather(city)

    if "error" in weather:
        return weather

    # NOTE: you don’t have rainfall in API → assume 0 for now
    rainfall = 0

    risks = predict_risks(
        weather["temperature"],
        weather["humidity"],
        rainfall,
        weather["wind_speed"]
    )

    advisory = generate_advisory(risks, weather)

    return {
        "weather": weather,
        "risks": risks,
        "advisory": advisory
    }


# 4. FLASK ROUTES
@app.route('/')
def home():
    return "KrishiMitra मौसम सलाह API चालू है 🚜"


@app.route('/weather_advisory', methods=['GET'])
def weather_advisory():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "कृपया शहर का नाम दर्ज करें"}), 400

    result = get_weather_advisory(city)

    if "error" in result:
        return jsonify(result), 500

    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )


# 5. RUN SERVER

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))