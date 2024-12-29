// services/orderApi.js
import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api/orders';


export const orderApi = {
  getCustomerOrders: async (customerId) => {
    try {
        const response = await axios.get(`${BASE_URL}/customer/${customerId}`);
        console.log('API Response:', response.data); // Debug log
        return response.data;
    } catch (error) {
        console.error('Error fetching orders:', error);
        throw error;
    }
  },

  getOrderDetails: async (orderId) => {
      try {
          const response = await axios.get(`${BASE_URL}/${orderId}`);
          return response.data;
      } catch (error) {
          console.error('Error fetching order details:', error);
          throw error;
      }
  }
};

// Helper Functions for Order API Operations
export const getAllOrders = async () => {
  try {
    const response = await axios.get(`${API_URL}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to fetch orders';
  }
};

export const getOrderById = async (orderId) => {
  try {
    const response = await axios.get(`${API_URL}/${orderId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to fetch order details';
  }
};

export const createOrderWithItems = async (orderData) => {
  try {
    const response = await axios.post(`${API_URL}`, orderData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to create order';
  }
};

export const updateOrder = async (orderId, orderData) => {
  try {
    const response = await axios.put(`${API_URL}/${orderId}`, orderData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to update order';
  }
};

export const deleteOrder = async (orderId) => {
  try {
    const response = await axios.delete(`${API_URL}/${orderId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to delete order';
  }
};

// Order Items operations
export const getOrderItems = async (orderId) => {
  try {
    const response = await axios.get(`${API_URL}/${orderId}/items`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to fetch order items';
  }
};

export const addOrderItem = async (orderId, itemData) => {
  try {
    const response = await axios.post(`${API_URL}/${orderId}/items`, itemData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to add order item';
  }
};

export const updateOrderItem = async (orderItemId, itemData) => {
  try {
    const response = await axios.put(`/api/order_items/${orderItemId}`, itemData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to update order item';
  }
};

export const deleteOrderItem = async (orderItemId) => {
  try {
    const response = await axios.delete(`/api/order_items/${orderItemId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to delete order item';
  }
};
