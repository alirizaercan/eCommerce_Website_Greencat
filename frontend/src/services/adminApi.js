import axios from 'axios';

const API_URL = 'http://localhost:5000/api/admin';

const VALID_GRAPH_TYPES = [
    "Gelir Analizi", "Ürün Satışları", 
    "Müşteri Aktivitesi", "Sipariş Durumu",
    "Kategori Performansı"
];

export const adminApi = {
    login: async (credentials) => {
        try {
            const response = await axios.post(`${API_URL}/login`, credentials);
            return response.data;
        } catch (error) {
            console.error('Login error:', error);
            throw new Error(error.response?.data?.message || 'Login failed');
        }
    },

    getGraphData: async (payload) => {
        try {
            if (!VALID_GRAPH_TYPES.includes(payload.graph_type)) {
                throw new Error(`Invalid graph type. Valid types are: ${VALID_GRAPH_TYPES.join(', ')}`);
            }

            const response = await axios.post(`${API_URL}/graphs/data`, payload);
            return response.data;
        } catch (error) {
            console.error('Error fetching graph data:', error);
            throw new Error(error.response?.data?.message || 'Failed to fetch graph data');
        }
    },

    generateGraph: async (payload) => {
        try {
            if (!VALID_GRAPH_TYPES.includes(payload.graph_type)) {
                throw new Error(`Invalid graph type. Valid types are: ${VALID_GRAPH_TYPES.join(', ')}`);
            }
    
            if (!payload.start_date || !payload.end_date) {
                throw new Error('Start date and end date are required');
            }
    
            const response = await axios.post(`${API_URL}/graphs/generate`, payload);
            return response.data;
            
        } catch (error) {
            console.error('Error generating graph:', error);
            return {
                success: false,
                message: error.response?.data?.message || error.message
            };
        }
    }
};

export default adminApi;