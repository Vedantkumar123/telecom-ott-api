const API_BASE_URL = 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const subscribeToPlan = async (planId) => {
  const response = await fetch(`${API_BASE_URL}/subscriptions/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ plan_id: planId }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Subscription failed');
  }

  return data;
};

export const getMySubscriptions = async () => {
  const response = await fetch(`${API_BASE_URL}/subscriptions/my`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Failed to fetch subscriptions');
  }

  return data;
};