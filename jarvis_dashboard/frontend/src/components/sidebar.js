// src/components/Sidebar.js
import React from 'react';
import '../styles/Sidebar.css';

function Sidebar({ availableWidgets, addWidget }) {
  return (
    <div className="sidebar">
      <h2>Widgets</h2>
      <ul>
        {availableWidgets.map((widget) => (
          <li key={widget.id}>
            {widget.name} <button onClick={() => addWidget(widget.id)}>Add</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;
