from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Simulate a user count (could be from a database in real projects)
current_count = 100

@app.route("/")
def home():
    return render_template("index.html", initial_count=current_count)

@app.route("/api/users/count")
def user_count():
    global current_count
    # Simulate user count increment
    increment = random.randint(0, 5)  
    current_count += increment
    return jsonify({"count": current_count})

if __name__ == "__main__":
    app.run(debug=True)
