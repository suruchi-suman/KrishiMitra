# 🌾 KrishiMitra - Weather Based Advisory for Farmers

KrishiMitra is a simple web-based application that provides **weather information and smart farming advisory** based on the selected city.

It helps farmers make better decisions by analyzing weather conditions and suggesting precautions and actions.

---

## 🚀 Live Demo

🔗 Frontend (GitHub Pages):  
https://your-username.github.io/your-repo-name/

🔗 Backend (Render API):  
https://krishimitra-szdo.onrender.com/weather_advisory?city=Jaipur

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS (Responsive Design)
- JavaScript (Fetch API)

### Backend
- Python
- Flask
- Machine Learning (Scikit-learn)

### Deployment
- Frontend: GitHub Pages
- Backend: Render

---

## ✨ Features

- 🔍 Search weather by city name
- 🌦 Displays real-time weather data:
  - Temperature
  - Humidity
  - Wind Speed
  - Condition
- ⚠ Identifies potential agricultural risks
- 📢 Provides AI-based farming advisory
- 📱 Fully responsive design (mobile-friendly)

---

## ⚙️ How It Works

1. User enters a city name on the frontend  
2. Frontend sends request to backend API: /weather_advisory?city=CityName
3. Backend:
- Fetches weather data
- Runs ML model for risk prediction
- Generates advisory  
4. Response is displayed on UI  

---

## 🧪 Run Locally

### 1. Clone Repository

### 2. Install Dependencies : pip install -r requirements.txt

### 3. Run Backend : python main.py

### 4. Open Frontend
Just open `index.html` in your browser

---

## ⚠️ Important Notes

- Backend must be running OR deployed for frontend to work  
- Free hosting platforms (Render) may be slow due to cold starts  
- Ensure correct API URL is used in `index.html`  

---

## 🐛 Common Issues

### ❌ Server error / Loading forever
- Backend is sleeping (Render free tier)  
- First request may take 30–60 seconds  

### ❌ CORS issues
- Make sure Flask has CORS enabled: from flask_cors import CORS
CORS(app)

---

## 🔮 Future Improvements

- 📍 Auto-detect user location  
- 🌱 Crop-specific recommendations  
- 📊 Dashboard for analytics  
- 🧠 Better ML model accuracy  
- 🌐 Multi-language support  

---

## 👩‍💻 Author

Suruchi Suman  

---

## 📜 License

This project is for educational and hackathon purposes.
