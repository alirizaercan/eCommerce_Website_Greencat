// frontend/src/services/auth.js

import axios from 'axios';

const API_URL = "http://localhost:5000/auth";

export const registerCustomer = async (customerData) => {
  try {
    const response = await axios.post(`${API_URL}/register`, customerData);
    return response.data;
  } catch (error) {
    return error.response.data;
  }
};

export const loginCustomer = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, credentials);
    return response.data;
  } catch (error) {
    return error.response.data;
  }
};

export const getCustomerById = async (customerId) => {
  try {
    const response = await axios.get(`${API_URL}/customer/${customerId}`);
    return response.data;
  } catch (error) {
    return error.response.data;
  }
};

export const updateCustomer = async (customerId, updates) => {
  try {
    const response = await axios.put(`${API_URL}/customer/${customerId}`, updates);
    return response.data;
  } catch (error) {
    return error.response.data;
  }
};

export const deleteCustomer = async (customerId) => {
  try {
    const response = await axios.delete(`${API_URL}/customer/${customerId}`);
    return response.data;
  } catch (error) {
    return error.response.data;
  }
};
