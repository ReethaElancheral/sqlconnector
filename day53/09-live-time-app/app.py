from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/time")
def get_time():
    now = datetime.now()
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d")
    })

if __name__ == "__main__":
    app.run(debug=True)
