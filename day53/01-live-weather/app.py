from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "6b8475d1939bb5502208fc73e60459e5"
CITY = "Doha,QA"

@app.route("/")
def index():
    return render_template("index.html", title="Live Weather Dashboard", location=CITY)

@app.route("/api/weather")
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    weather_data = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "status": data["weather"][0]["main"]
    }
    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)
