from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# In-memory task storage
tasks = []

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks, title="Task Manager App")

# API endpoints
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "title": data["title"]
    }
    tasks.append(task)
    return jsonify({"message": "Task added", "task": task}), 201

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
