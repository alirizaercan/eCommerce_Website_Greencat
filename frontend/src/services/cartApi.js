import axios from 'axios';

const API_URL = 'http://localhost:5000/api/cart';

export const addItemToCart = async (sessionId, productId, quantity = 1) => {
  try {
    const response = await axios.post(API_URL, {
      session_id: sessionId,
      product_id: productId,
      quantity: quantity
    });
    return response.data;
  } catch (error) {
    console.error('Add to cart error:', error.response?.data || error.message);
    throw error;
  }
};

export const getCartItems = async (sessionId) => {
  try {
    const response = await axios.get(`${API_URL}/${sessionId}/summary`);
    return response.data;
  } catch (error) {
    console.error('Get cart items error:', error.response?.data || error.message);
    throw error;
  }
};

export const updateCartItem = async (cartItemId, quantity) => {
  try {
    const response = await axios.put(`${API_URL}/item/${cartItemId}`, { quantity });
    return response.data;
  } catch (error) {
    console.error('Update cart item error:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteCartItem = async (cartItemId) => {
  try {
    const response = await axios.delete(`${API_URL}/item/${cartItemId}`);
    if (response.status === 200) {
      return {
        success: true,
        cartItemId: response.data.cart_item_id
      };
    }
    throw new Error('Failed to delete item');
  } catch (error) {
    console.error('Delete cart item error:', error.response?.data || error.message);
    throw error;
  }
};