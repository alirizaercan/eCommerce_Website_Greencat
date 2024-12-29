import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api/carrier';

export const carrierApi = {
    getOrderCarrier: async (orderId) => {
        try {
            const response = await axios.get(`${BASE_URL}/order/${orderId}/carrier`);
            return response.data;
        } catch (error) {
            console.error('Error fetching carrier info:', error);
            return { carrier_name: 'Not Available' };
        }
    }
};