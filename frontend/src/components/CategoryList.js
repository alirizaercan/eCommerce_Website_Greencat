import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import categoryApi from "../services/categoryApi";

const CategoryList = () => {
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        categoryApi.getCategories()
            .then(response => setCategories(response.data))
            .catch(error => console.error("Error fetching categories:", error));
    }, []);

    return (
        <ul>
            {categories.map(category => (
                <li key={category.id}>
                    <Link to={`/category/${category.name}`}>{category.name}</Link>
                </li>
            ))}
        </ul>
    );
};

export default CategoryList;
