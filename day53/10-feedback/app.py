from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory feedback storage
feedbacks = []

@app.route("/")
def home():
    return render_template("index.html", feedbacks=feedbacks)

@app.route("/api/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json()
    name = data.get("name")
    message = data.get("message")

    if not name or not message:
        return jsonify({"status": "error", "message": "Name and message are required"}), 400

    feedbacks.append({"name": name, "message": message})
    return jsonify({"status": "success", "message": "Thank you for your feedback!"})

@app.route("/api/feedbacks", methods=["GET"])
def get_feedbacks():
    return jsonify(feedbacks)

if __name__ == "__main__":
    app.run(debug=True)
