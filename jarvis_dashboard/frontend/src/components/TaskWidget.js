// src/components/TaskWidget.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/TaskWidget.css';

function TaskWidget() {
  const [tasks, setTasks] = useState([]);
  const [newTaskDesc, setNewTaskDesc] = useState('');
  const [newTaskDue, setNewTaskDue] = useState('');
  const [newTaskStatus, setNewTaskStatus] = useState('not started');

  // Function to fetch tasks from the backend
  const fetchTasks = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/tasks?cb=${Date.now()}`);
      console.log('Fetched tasks:', res.data);
      setTasks(res.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // Poll tasks every 3 seconds
  useEffect(() => {
    fetchTasks(); // initial fetch
    const intervalId = setInterval(fetchTasks, 3000);
    return () => clearInterval(intervalId);
  }, []);

  const handleAddTask = async () => {
    if (!newTaskDesc.trim() || !newTaskDue.trim()) return;
    try {
      await axios.post('http://127.0.0.1:5000/api/tasks', {
        description: newTaskDesc,
        due_date: newTaskDue,
        status: newTaskStatus,
      });
      setNewTaskDesc('');
      setNewTaskDue('');
      setNewTaskStatus('not started');
      fetchTasks(); // update after adding
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  const handleUpdateTaskStatus = async (taskId, updatedStatus) => {
    try {
      await axios.put(`http://127.0.0.1:5000/api/tasks/${taskId}`, {
        status: updatedStatus,
      });
      fetchTasks();
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/tasks/${taskId}`);
      fetchTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  return (
    <div className="task-widget">
      <h2>To-Do List</h2>
      <div className="new-task">
        <input
          type="text"
          placeholder="Task description..."
          value={newTaskDesc}
          onChange={(e) => setNewTaskDesc(e.target.value)}
        />
        <input
          type="datetime-local"
          placeholder="Due date/time..."
          value={newTaskDue}
          onChange={(e) => setNewTaskDue(e.target.value)}
        />
        <select value={newTaskStatus} onChange={(e) => setNewTaskStatus(e.target.value)}>
          <option value="not started">Not Started</option>
          <option value="barely started">Barely Started</option>
          <option value="started">Started</option>
          <option value="in progress">In Progress</option>
          <option value="near completion">Near Completion</option>
          <option value="done">Done</option>
        </select>
        <button onClick={handleAddTask}>Add Task</button>
      </div>
      <ul className="task-list">
        {tasks
          .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
          .map(task => (
          <li key={task.id} className={`task-item ${task.status.replace(/\s/g, '-')}`}>
            <div className="task-info">
              <span className="task-desc">{task.description}</span>
              <span className="task-due">Due: {task.due_date}</span>
              <span className={`task-status ${task.status.replace(/\s/g, '-').toLowerCase()}`}>
                Status: {task.status}
              </span>
            </div>
            <div className="task-actions">
              {task.status !== "done" && (
                <button onClick={() => handleUpdateTaskStatus(task.id, "done")}>Mark Done</button>
              )}
              <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskWidget;
