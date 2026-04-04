import React, { useState, useEffect } from 'react';
import { getAccessHistory } from '../api/accessApi';

const AccessHistory = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getAccessHistory();
        setHistory(data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>Access History</h2>
      {error && <p>{error}</p>}
      <ul>
        {history.map(item => (
          <li key={item._id}>
            Content ID: {item.content_id} - Accessed at: {new Date(item.watched_at).toLocaleString()}
          </li>
        ))}
      </ul>
      <a href="/dashboard">Back to Dashboard</a>
    </div>
  );
};

export default AccessHistory;