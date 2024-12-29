import axios from 'axios';

const API_URL = 'http://localhost:5000/api/sessions';
const TIMEOUT = 5000;

export const createSession = async (sessionData) => {
  try {
    const response = await axios.post(API_URL + '/', sessionData, { timeout: TIMEOUT });
    return response.data?.session || null;
  } catch (error) {
    console.error('Create session error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Failed to create session');
  }
};

export const getSessionById = async (sessionId) => {
  try {
    const response = await axios.get(`${API_URL}/${sessionId}`, { timeout: TIMEOUT });
    return response.data || null;
  } catch (error) {
    console.error('Get session error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Failed to get session');
  }
};

export const updateSession = async (sessionId, sessionData) => {
  try {
    const response = await axios.put(`${API_URL}/${sessionId}`, sessionData, { timeout: TIMEOUT });
    return response.data?.session || null;
  } catch (error) {
    console.error('Update session error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Failed to update session');
  }
};

export const deleteSession = async (sessionId) => {
  try {
    const response = await axios.delete(`${API_URL}/${sessionId}`, { timeout: TIMEOUT });
    return response.data?.message || null;
  } catch (error) {
    console.error('Delete session error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Failed to delete session');
  }
};