import axios from "axios";

const API_URL = "http://localhost:5000/api/products";

export const getRandomProducts = async () => {
  try {
    const response = await axios.get(`${API_URL}/random`);
    return response.data;
  } catch (error) {
    console.error("Error fetching random products:", error);
    return [];
  }
};

export const updateProduct = async (productId, productData) => {
  const response = await axios.put(`${API_URL}/${productId}`, productData);
  return response.data;
};

export const deleteProduct = async (productId) => {
  const response = await axios.delete(`${API_URL}/${productId}`);
  return response.data;
};

export const getProductsByCategory = async (categoryId) => {
  const response = await axios.get(`${API_URL}/category/${categoryId}`);
  return response.data;
};

export const searchProducts = async (searchTerm) => {
  try {
    const response = await axios.get(`${API_URL}/search`, {
      params: { term: searchTerm }
    });
    return response.data;
  } catch (error) {
    console.error("Error searching products:", error);
    return [];
  }
};