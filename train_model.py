# Generating dataset - Establishing manual rules to create dataset
import pandas as pd
import numpy as np

data = []

for _ in range(2000):
    temp = np.random.uniform(5, 45)
    humidity = np.random.uniform(10, 100)
    rainfall = np.random.uniform(0, 300)
    wind = np.random.uniform(0, 50)

    # Define risks (logic ONLY for training data)
    heat_stress = 1 if temp > 35 else 0
    low_moisture = 1 if humidity < 30 and rainfall < 20 else 0
    flood_risk = 1 if rainfall > 200 else 0
    fungal_risk = 1 if humidity > 80 and temp > 20 else 0
    cold_stress = 1 if temp < 10 else 0

    data.append([temp, humidity, rainfall, wind,
                 heat_stress, low_moisture, flood_risk, fungal_risk, cold_stress])

df = pd.DataFrame(data, columns=[
    "temp", "humidity", "rainfall", "wind",
    "heat_stress", "low_moisture", "flood_risk", "fungal_risk", "cold_stress"
])

df.to_csv("weather_risk_dataset.csv", index=False)

#Train ML model - multi label
# 1. Splitting Data
from sklearn.model_selection import train_test_split

X = df[["temp", "humidity", "rainfall", "wind"]]
y = df[["heat_stress", "low_moisture", "flood_risk", "fungal_risk", "cold_stress"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 2. Training Data
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)

# 3. Evaluate Model
from sklearn.metrics import accuracy_score

pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))


import joblib
joblib.dump(model, "risk_model.pkl")