from dotenv import load_dotenv
import os
from llmBasedAdvisory import generate_advisory

load_dotenv()

import requests
from flask import Flask, request, jsonify
import json
from flask import Response

app = Flask(__name__)
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

model = joblib.load("risk_model.pkl")

# 3. PREDICTION FUNCTION

def predict_risks(temp, humidity, rainfall, wind):
    input_data = [[temp, humidity, rainfall, wind]]
    pred = model.predict(input_data)[0]

    labels = ["heat_stress", "low_moisture", "flood_risk", "fungal_risk", "cold_stress"]

    return [labels[i] for i in range(len(labels)) if pred[i] == 1]



def get_weather_advisory(city):
    weather = get_weather(city)

    if "error" in weather:
        return weather

    rainfall = 0  

    risks = predict_risks(
        weather["temperature"],
        weather["humidity"],
        rainfall,
        weather["wind_speed"]
    )

    # ✅ Prepare full weather data for LLM (including wind)
    weather_for_llm = {
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "rainfall": rainfall,
        "wind_speed": weather["wind_speed"]
    }

    try:
        advisory = generate_advisory(risks, weather_for_llm)
    except Exception as e:
        print("LLM Error:", e)
        advisory = "मौसम के अनुसार सिंचाई और फसल की देखभाल करें।"
    
    print("WEATHER:", weather_for_llm)
    print("RISKS:", risks)
    print("ADVISORY:", advisory)
    
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

    return Response(json.dumps(result, ensure_ascii=False),content_type='application/json; charset=utf-8')


# 5. RUN SERVER

if __name__ == '__main__':
    app.run(debug=True)