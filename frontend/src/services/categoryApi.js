import axios from "axios";

const categoryApi = {
    getCategories: () => axios.get("/categories/"),
    getCategoryById: (id) => axios.get(`/categories/${id}`),
};

export default categoryApi;
