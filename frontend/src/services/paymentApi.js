import axios from 'axios';

const API_URL = 'http://localhost:5000/api/payments';

export const createPayment = async (paymentData) => {
  const response = await axios.post(API_URL, paymentData);
  return response.data;
};


export const processPayment = async (paymentData) => {
  try {
    const response = await axios.post(`${API_URL}/process`, {
      amount: Number(paymentData.amount),
      card_type: paymentData.cardType,
      card_number: paymentData.cardNumber?.replace(/-/g, '') || '',
      card_holder: paymentData.cardHolder,
      expiry_date: paymentData.expiryDate,
      cvv: paymentData.cvv
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Payment failed');
  }
};

export const getAllPayments = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getPaymentById = async (paymentId) => {
  const response = await axios.get(`${API_URL}/${paymentId}`);
  return response.data;
};

export const updatePayment = async (paymentId, paymentData) => {
  const response = await axios.put(`${API_URL}/${paymentId}`, paymentData);
  return response.data;
};

export const deletePayment = async (paymentId) => {
  const response = await axios.delete(`${API_URL}/${paymentId}`);
  return response.data;
};