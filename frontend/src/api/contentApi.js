const API_BASE_URL = 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const getContent = async () => {
  const response = await fetch(`${API_BASE_URL}/content/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to fetch content');
  }
  return data;
};

export const addContent = async (contentData) => {
  const response = await fetch(`${API_BASE_URL}/content/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(contentData),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to add content');
  }
  return data;
};