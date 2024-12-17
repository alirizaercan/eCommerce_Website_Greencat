import axios from "axios";

const productApi = {
    getProductsByCategory: (categoryName) => 
        axios.get(`/products?category=${encodeURIComponent(categoryName)}`),
};

export default productApi;
