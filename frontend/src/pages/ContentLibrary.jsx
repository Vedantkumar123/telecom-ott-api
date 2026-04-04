import React, { useState, useEffect } from 'react';
import { getContent } from '../api/contentApi';
import { accessContent } from '../api/accessApi';

const ContentLibrary = () => {
  const [content, setContent] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const data = await getContent();
        setContent(data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchContent();
  }, []);

  const handleAccess = async (contentId) => {
    try {
      const data = await accessContent(contentId);
      alert('Content accessed: ' + JSON.stringify(data));
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div>
      <h2>Content Library</h2>
      {error && <p>{error}</p>}
      <ul>
        {content.map(item => (
          <li key={item._id}>
            {item.title} - {item.platform} ({item.category})
            <button onClick={() => handleAccess(item._id)}>Access</button>
          </li>
        ))}
      </ul>
      <a href="/dashboard">Back to Dashboard</a>
    </div>
  );
};

export default ContentLibrary;