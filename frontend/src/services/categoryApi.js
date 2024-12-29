import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api/categories';

export const categoryApi = {
    getAllCategories: async () => {
        try {
            const response = await axios.get(`${BASE_URL}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    },

    getCategoryProducts: async (categoryId) => {
        try {
            const response = await axios.get(`${BASE_URL}/${categoryId}/products`);
            return response.data;
        } catch (error) {
            console.error('Error fetching category products:', error);
            throw error;
        }
    }
};