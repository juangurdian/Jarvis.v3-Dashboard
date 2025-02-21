// src/components/Dashboard.js
import React, { useState } from 'react';
import Sidebar from './sidebar.js';
import ChatWidget from './chatWidget.js';
import TaskWidget from './TaskWidget.js';
import PlaceholderWidget from './PlaceholderWidget.js';
import NewsWidget from './NewsWidget.js';
import CryptoWidget from './CryptoWidget.js';
import '../styles/Dashboard.css';

// Define available widgets and their corresponding components.
const availableWidgets = [
  { id: 'chat', name: 'Chat', component: ChatWidget },
  { id: 'tasks', name: 'Tasks', component: TaskWidget },
  { id: 'calendar', name: 'Calendar', component: PlaceholderWidget },
  { id: 'weather', name: 'Weather', component: PlaceholderWidget },
  { id: 'stocks', name: 'Stocks', component: PlaceholderWidget },
  { id: 'crypto', name: 'Crypto', component: CryptoWidget },
  { id: 'news', name: 'News', component: NewsWidget },
  { id: 'images', name: 'Images', component: PlaceholderWidget },
];

function Dashboard() {
  // Start with a few active widgets (you can adjust the default list).
  const [activeWidgets, setActiveWidgets] = useState(['chat', 'tasks', 'calendar']);

  const addWidget = (widgetId) => {
    if (!activeWidgets.includes(widgetId)) {
      setActiveWidgets([...activeWidgets, widgetId]);
    }
  };

  const removeWidget = (widgetId) => {
    setActiveWidgets(activeWidgets.filter((id) => id !== widgetId));
  };

  const renderWidget = (widgetId) => {
    const widget = availableWidgets.find((w) => w.id === widgetId);
    if (!widget) return null;
    const Component = widget.component;
    // Add a special CSS class if the widget is "tasks"
    const widgetClass = widget.id === 'tasks' ? "widget tasks-widget" : "widget";
    return (
      <div key={widget.id} className={widgetClass}>
        <div className="widget-header">
          <h3>{widget.name}</h3>
          <button onClick={() => removeWidget(widget.id)}>X</button>
        </div>
        <div className="widget-body">
          <Component />
        </div>
      </div>
    );
  };

  return (
    <div className="dashboard">
      <Sidebar availableWidgets={availableWidgets} addWidget={addWidget} />
      <div className="widgets-container">
        {activeWidgets.map(renderWidget)}
      </div>
    </div>
  );
}

export default Dashboard;
