import { useEffect, useState } from "react";
import axios from "axios";

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [message, setMessage] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [editTaskId, setEditTaskId] = useState(null);

  const token = localStorage.getItem("token");

  const fetchTasks = () => {
    if (!token) {
      setMessage("Unauthorized. Please log in.");
      return;
    }

    axios
      .get("http://127.0.0.1:8000/tasks", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setTasks(res.data))
      .catch(() => setMessage("Failed to load tasks ❌"));
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const taskData = { title, description };

    if (editTaskId) {
      // Update task
      axios
        .put(`http://127.0.0.1:8000/tasks/${editTaskId}`, taskData, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          setEditTaskId(null);
          setTitle("");
          setDescription("");
          fetchTasks();
        });
    } else {
      // Create new task
      axios
        .post("http://127.0.0.1:8000/tasks", taskData, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          setTitle("");
          setDescription("");
          fetchTasks();
        });
    }
  };

  const handleDelete = (id) => {
    axios
      .delete(`http://127.0.0.1:8000/tasks/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => fetchTasks());
  };

  const handleEdit = (task) => {
    setEditTaskId(task.id);
    setTitle(task.title);
    setDescription(task.description);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Tasks</h2>

      <form onSubmit={handleSubmit} className="mb-6">
        <input
          type="text"
          placeholder="Title"
          className="w-full p-2 border mb-2"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          className="w-full p-2 border mb-2"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded mr-2">
          {editTaskId ? "Update Task" : "Add Task"}
        </button>
        {editTaskId && (
          <button
            type="button"
            onClick={() => {
              setEditTaskId(null);
              setTitle("");
              setDescription("");
            }}
            className="bg-gray-500 text-white py-2 px-4 rounded"
          >
            Cancel
          </button>
        )}
      </form>

      {message && <p>{message}</p>}

      <ul className="space-y-2">
        {tasks.map((task) => (
          <li
            key={task.id}
            className="border p-3 rounded shadow flex justify-between items-center"
          >
            <div>
              <strong>{task.title}</strong>: {task.description}
            </div>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(task)}
                className="bg-yellow-400 px-2 py-1 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(task.id)}
                className="bg-red-500 text-white px-2 py-1 rounded"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tasks;
