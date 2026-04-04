const API_BASE_URL = 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const accessContent = async (contentId) => {
  const response = await fetch(`${API_BASE_URL}/access/${contentId}`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to access content');
  }
  return data;
};

export const getAccessHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/access/history`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to fetch access history');
  }
  return data;
};