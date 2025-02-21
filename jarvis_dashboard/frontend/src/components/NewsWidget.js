// src/components/NewsWidget.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/NewsWidget.css';

function NewsWidget() {
  const [articles, setArticles] = useState([]);
  const [query, setQuery] = useState('');

  // Function to fetch news from the backend
  const fetchNews = async () => {
    try {
      // Adding a cache-busting query parameter to avoid caching issues
      const res = await axios.get(`http://127.0.0.1:5000/api/news?cb=${Date.now()}`, {
        params: { query }
      });
      console.log("Fetched news:", res.data);
      setArticles(res.data.articles);
    } catch (error) {
      console.error("Error fetching news:", error);
    }
  };

  // Poll news every 60 seconds
  useEffect(() => {
    fetchNews(); // initial fetch
    const intervalId = setInterval(fetchNews, 60000); // update every 60 seconds
    return () => clearInterval(intervalId);
  }, [query]);

  return (
    <div className="news-widget">
      <h2>Latest News</h2>
      <div className="news-search">
        <input 
          type="text" 
          placeholder="Search news..." 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={fetchNews}>Search</button>
      </div>
      <div className="news-list">
        {articles.length === 0 ? (
          <p>No articles found.</p>
        ) : (
          articles.map((article, index) => (
            <div key={index} className="news-item">
              <h3>{article.title}</h3>
              <p>{article.description}</p>
              <a href={article.url} target="_blank" rel="noreferrer">Read More</a>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default NewsWidget;
