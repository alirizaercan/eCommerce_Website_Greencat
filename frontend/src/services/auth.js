import axios from 'axios';
const API_URL = "http://localhost:5000/api/auth";

export const registerCustomer = async (customerData) => {
  try {
    const response = await axios.post(`${API_URL}/register`, customerData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || "An error occurred");
  }
};

export const loginCustomer = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, credentials);
    if (response.data.isLoggedIn && response.data.customer_id) {
      // No need to make a separate call to getCustomerById since login now returns all info
      return response.data;
    }
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || "Login failed");
  }
};

export const logoutCustomer = async () => {
  try {
    const customerId = localStorage.getItem('customerId');
    if (customerId) {
      const response = await axios.post(`${API_URL}/logout`, { customer_id: customerId });
      if (response.data.message === "Logged out successfully") {
        localStorage.clear(); // Clear all auth-related items
        return response.data;
      }
    }
    return { message: "No active session" };
  } catch (error) {
    throw new Error(error.response?.data?.message || "Logout failed");
  }
};

export const getCustomerById = async (customerId) => {
  try {
    const response = await axios.get(`${API_URL}/customer/${customerId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customer by ID", error);
    return {};
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