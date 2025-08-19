from flask import Flask, jsonify, send_from_directory
import requests
import os
import random

app = Flask(__name__, static_folder="build", static_url_path="/")

# Fallback quotes in case API fails
fallback_quotes = [
    "The best way to get started is to quit talking and begin doing.",
    "Don’t let yesterday take up too much of today.",
    "It’s not whether you get knocked down, it’s whether you get up.",
    "If you are working on something exciting, it will keep you motivated."
]

@app.route("/api/quote")
def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=5)
        res.raise_for_status()
        data = res.json()
        quote = f"{data['content']} — {data['author']}"
        return jsonify({"quote": quote})
    except Exception as e:
        print("Error fetching quote:", e)
        # Return random fallback quote
        return jsonify({"quote": random.choice(fallback_quotes)})

# Serve React build
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(f"build/{path}"):
        return send_from_directory("build", path)
    else:
        return send_from_directory("build", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
