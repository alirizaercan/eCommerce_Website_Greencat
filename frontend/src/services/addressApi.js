/* frontend/src/services/addressApi.js */

import axios from 'axios';

const API_URL = 'http://localhost:5000/api/customer';

export const addressApi = {
  getAddresses: async (customerId) => {
    try {
      const response = await axios.get(`${API_URL}/${customerId}/addresses`);
      return response.data.addresses;
    } catch (error) {
      console.error('Get addresses error:', error);
      throw error;
    }
  },

  createAddress: async (customerId, addressData) => {
    try {
      const response = await axios.post(`${API_URL}/${customerId}/addresses`, {
        address_line1: addressData.address_line1,
        address_line2: addressData.address_line2,
        city: addressData.city,
        postal_code: addressData.postal_code,
        country: addressData.country,
        phone_number: addressData.phone_number,
        address_type: addressData.address_type
      });
      return response.data;
    } catch (error) {
      console.error('Create address error:', error);
      throw error;
    }
  },

  updateAddress: async (addressId, addressData) => {
    try {
      const response = await axios.put(`${API_URL}/addresses/${addressId}`, {
        address_line1: addressData.street,
        address_line2: addressData.district,
        city: addressData.city,
        postal_code: addressData.postalCode,
        country: addressData.country || 'Türkiye',
        phone_number: addressData.phone
      });
      return response.data;
    } catch (error) {
      console.error('Update address error:', error);
      throw error;
    }
  },

  deleteAddress: async (addressId) => {
    try {
      const response = await axios.delete(`${API_URL}/addresses/${addressId}`);
      return response.data;
    } catch (error) {
      console.error('Delete address error:', error);
      throw error;
    }
  }
};
