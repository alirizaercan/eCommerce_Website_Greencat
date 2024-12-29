import axios from 'axios';

const API_URL = 'http://localhost:5000/api/checkout';

export const validateCheckout = async (customerId, sessionId) => {
  try {
    if (!customerId || !sessionId) {
      return { success: false, error: 'Missing required information' };
    }

    const response = await axios.post(`${API_URL}/validate`, {
      customer_id: customerId,
      session_id: sessionId
    });

    if (response.data.success && response.data.summary) {
      const summary = response.data.summary;
      return {
        ...response.data,
        summary: {
          ...summary,
          subtotal: Number(summary.subtotal),
          tax: Number(summary.tax),
          total: Number(summary.total)
        }
      };
    }

    return response.data;
  } catch (error) {
    console.error('Checkout validation error:', error);
    throw new Error(error.response?.data?.error || 'Checkout validation failed');
  }
};

export const processCheckout = async (checkoutData) => {
  try {
    const payload = {
      customer_id: checkoutData.customer_id,
      session_id: checkoutData.session_id,
      address_id: checkoutData.address_id,
      payment: {
        amount: Number(checkoutData.payment.amount || 0),
        card_number: String(checkoutData.payment.card_number || '').replace(/\s+/g, ''),
        card_holder: String(checkoutData.payment.card_holder || ''),
        expiry_date: String(checkoutData.payment.expiry_date || ''),
        cvv: String(checkoutData.payment.cvv || '')
      }
    };

    const response = await axios.post('http://localhost:5000/api/checkout/process', payload);
    return response.data;
  } catch (error) {
    console.error('Checkout error:', error);
    throw new Error(error.response?.data?.error || 'Checkout failed');
  }
};

export const getCheckoutSummary = async (customerId, sessionId) => {
  try {
    const response = await axios.get(`${API_URL}/summary`, {
      params: { customer_id: customerId, session_id: sessionId }
    });
    
    if (!response.data.success) {
      throw new Error(response.data.error || 'Failed to fetch checkout summary');
    }
    
    return response.data;
  } catch (error) {
    console.error('Get checkout summary error:', error);
    throw new Error(error.response?.data?.error || 'Failed to fetch checkout summary');
  }
};

export const finalizeOrder = async (orderData) => {
  try {
    const response = await axios.post(`${API_URL}/finalize`, orderData);
    return response.data;
  } catch (error) {
    console.error('Finalize order error:', error);
    throw new Error(error.response?.data?.error || 'Order finalization failed');
  }
};