// src/components/CryptoWidget.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/CryptoWidget.css';

function CryptoWidget() {
  const [trending, setTrending] = useState([]);

  const fetchCrypto = async () => {
    try {
      // Cache busting parameter
      const res = await axios.get(`http://127.0.0.1:5000/api/crypto?cb=${Date.now()}`);
      console.log("Fetched crypto data:", res.data);
      // Assume the Dexscreener API returns a JSON object with a "pairs" key
      setTrending(res.data.pairs || []);
    } catch (error) {
      console.error("Error fetching crypto data:", error);
    }
  };

  // Poll for crypto data every 60 seconds
  useEffect(() => {
    fetchCrypto();
    const intervalId = setInterval(fetchCrypto, 60000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="crypto-widget">
      <h2>Trending Crypto</h2>
      {trending.length === 0 ? (
        <p>No trending data available.</p>
      ) : (
        <div className="crypto-list">
          {trending.map((pair, index) => (
            <div key={index} className="crypto-item">
              <h3>{pair.baseToken.symbol} / {pair.quoteToken.symbol}</h3>
              <p>{pair.baseToken.name}</p>
              <p>Price: {pair.priceUsd ? Number(pair.priceUsd).toFixed(4) : 'N/A'} USD</p>
              {pair.txVolume ? (
                <p>Volume: {Number(pair.txVolume).toFixed(2)}</p>
              ) : null}
              <a href={pair.url} target="_blank" rel="noreferrer">View on Dexscreener</a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CryptoWidget;
