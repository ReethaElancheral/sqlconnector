from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Candidate votes
candidates = {
    "Alice": 0,
    "Bob": 0,
    "Charlie": 0
}

@app.route("/")
def home():
    return render_template("index.html", candidates=candidates)

@app.route("/api/vote", methods=["POST"])
def vote():
    data = request.get_json()
    candidate = data.get("candidate")
    if candidate in candidates:
        candidates[candidate] += 1
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid candidate"}), 400

@app.route("/api/results")
def results():
    return jsonify(candidates)

if __name__ == "__main__":
    app.run(debug=True)
