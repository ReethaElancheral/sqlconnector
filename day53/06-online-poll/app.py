from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Poll question and options
poll = {
    "question": "What is your favorite programming language?",
    "options": {"Python": 0, "JavaScript": 0, "Java": 0, "C++": 0}
}

@app.route("/")
def home():
    return render_template("index.html", poll=poll)

@app.route("/api/poll", methods=["GET"])
def get_poll():
    return jsonify({
        "question": poll["question"],
        "options": poll["options"]
    })

@app.route("/api/vote", methods=["POST"])
def vote():
    data = request.get_json()
    option = data.get("option")
    
    # Prevent double voting per session
    if session.get("voted", False):
        return jsonify({"status": "error", "message": "You already voted"}), 400

    if option in poll["options"]:
        poll["options"][option] += 1
        session["voted"] = True
        return jsonify({"status": "success", "options": poll["options"]})
    
    return jsonify({"status": "error", "message": "Invalid option"}), 400

if __name__ == "__main__":
    app.run(debug=True)
