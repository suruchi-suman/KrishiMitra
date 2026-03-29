from dotenv import load_dotenv
import os

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



# 2. FARMING ADVISORY LOGIC FUNCTION (HINDI)

def generate_advisory(temp, humidity, wind, condition):
    advice = []

    condition = condition.lower()

    # Rainy
    if condition == "rain":
        advice.append("आज बारिश की संभावना है। कीटनाशकों का छिड़काव न करें।")
        advice.append("आज सिंचाई की आवश्यकता नहीं है।")
        advice.append("खेत में जल निकासी की उचित व्यवस्था रखें।")

    # High Temperature
    if temp >= 35:
        advice.append("तापमान अधिक है। सुबह या शाम के समय सिंचाई करें।")
        advice.append("फसलों को गर्मी से बचाने के लिए मल्चिंग या छाया का उपयोग करें।")

    # High Humidity
    if humidity >= 80:
        advice.append("आर्द्रता अधिक है। फंगल रोगों का खतरा बढ़ सकता है।")
        advice.append("पत्तियों पर धब्बे या फफूंदी के लक्षणों की निगरानी करें।")

    # Windy
    if wind >= 10:
        advice.append("हवा की गति तेज है। कीटनाशकों का छिड़काव न करें।")
        advice.append("कमजोर पौधों को सहारा दें ताकि वे गिर न जाएं।")

    # Clear Weather
    if condition == "clear":
        advice.append("मौसम साफ है। खेती के अधिकांश कार्यों के लिए उपयुक्त समय है।")

    # Cloudy
    if condition == "clouds":
        advice.append("मौसम बादलों से घिरा है। कीटों की गतिविधियों पर नजर रखें।")

    # Default
    if not advice:
        advice.append("मौसम सामान्य है। नियमित खेती कार्य जारी रखें।")

    return advice



# 3. COMBINED FUNCTION

def get_weather_advisory(city):
    weather = get_weather(city)

    if "error" in weather:
        return weather

    temp = weather["temperature"]
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    condition = weather["condition"]

    advisory = generate_advisory(temp, humidity, wind, condition)

    result = {
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind,
        "condition": condition,
        "advisory": advisory
    }

    return result



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