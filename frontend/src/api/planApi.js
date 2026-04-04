const API_BASE_URL = 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const getPlans = async () => {
  const response = await fetch(`${API_BASE_URL}/plans/`, {
    method: 'GET',
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Failed to fetch plans');
  }

  return data;
};

export const createPlan = async (planData) => {
  const response = await fetch(`${API_BASE_URL}/plans/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(planData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Failed to create plan');
  }

  return data;
};