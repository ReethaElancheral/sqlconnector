const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");
const taskTable = document.getElementById("taskTable").querySelector("tbody");
const alertPlaceholder = document.getElementById("alertPlaceholder");

// Show bootstrap alert
function showAlert(message, type = "success") {
  alertPlaceholder.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>`;
}

// Fetch tasks and render table
async function fetchTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  taskTable.innerHTML = "";
  tasks.forEach(task => {
    const row = document.createElement("tr");
    row.setAttribute("data-id", task.id);
    row.innerHTML = `
      <td>${task.id}</td>
      <td>${task.title}</td>
      <td><button class="btn btn-danger btn-sm delete-btn">Delete</button></td>
    `;
    taskTable.appendChild(row);
  });
}

// Add new task
taskForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = taskInput.value.trim();
  if (!title) return showAlert("Task title cannot be empty", "danger");

  const res = await fetch("/api/tasks", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({title})
  });
  const data = await res.json();
  if (res.ok) {
    showAlert(data.message);
    taskInput.value = "";
    fetchTasks();
  } else {
    showAlert(data.error, "danger");
  }
});

// Delete task
taskTable.addEventListener("click", async (e) => {
  if (!e.target.classList.contains("delete-btn")) return;
  const row = e.target.closest("tr");
  const taskId = row.getAttribute("data-id");

  const res = await fetch(`/api/tasks/${taskId}`, { method: "DELETE" });
  const data = await res.json();
  if (res.ok) {
    showAlert(data.message);
    fetchTasks();
  } else {
    showAlert("Error deleting task", "danger");
  }
});

// Initial fetch
fetchTasks();
