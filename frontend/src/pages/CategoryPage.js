import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import productApi from "../services/productApi";
import CategoryList from "../components/CategoryList";
import ProductCard from "../components/ProductCard";

const CategoryPage = () => {
    const { categoryName } = useParams();
    const [products, setProducts] = useState([]);

    useEffect(() => {
        productApi.getProductsByCategory(categoryName)
            .then(response => setProducts(response.data))
            .catch(error => console.error("Error fetching products:", error));
    }, [categoryName]);

    return (
        <div>
            <h1>{categoryName} Kategorisi</h1>
            <CategoryList />
            <div className="product-grid">
                {products.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export default CategoryPage;
