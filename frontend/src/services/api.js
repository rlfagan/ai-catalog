import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchModels = async (params) => {
  try {
    const response = await api.get('/search', { params });
    return response.data;
  } catch (error) {
    console.error('Error searching models:', error);
    throw error;
  }
};

export const getModel = async (modelId) => {
  try {
    const response = await api.get(`/models/${encodeURIComponent(modelId)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching model:', error);
    throw error;
  }
};

export const getTrending = async (limit = 20) => {
  try {
    const response = await api.get('/trending', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('Error fetching trending:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export default api;
