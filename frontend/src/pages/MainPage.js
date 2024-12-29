import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { getRandomProducts } from "../services/productApi";
import { categoryApi } from "../services/categoryApi";
import ProductCard from "../components/ProductCard";
import "../styles/MainPage.css";

const MainPage = () => {
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [randomProducts, categoriesData] = await Promise.all([
                    getRandomProducts(),
                    categoryApi.getAllCategories()
                ]);
                setProducts(randomProducts);
                setCategories(categoriesData);
            } catch (error) {
                console.error("Veri yükleme hatası:", error);
                setError("İçerik yüklenemedi");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleCategoryClick = async (category) => {
        if (!category) {
            setSelectedCategory(null);
            const randomProducts = await getRandomProducts();
            setProducts(randomProducts);
            navigate('/');
            return;
        }

        try {
            setLoading(true);
            const slug = category.category_name.toLowerCase().replace(/\s+/g, '-');
            navigate(`/category/${slug}`);
            const products = await categoryApi.getCategoryProducts(category.category_id);
            setProducts(products);
            setSelectedCategory(category.category_id);
        } catch (error) {
            console.error("Hata:", error);
            setError("Ürünler yüklenemedi");
        } finally {
            setLoading(false);
        }
    };

    const chunkArray = (arr, size) => {
        return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
            arr.slice(i * size, i * size + size)
        );
    };

    const categoryRows = chunkArray(categories, 6);

    if (loading) return <div className="loading">Yükleniyor...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="main-page">
            <Header />
            <div className="category-section">
                <div className="category-grid">
                    <button
                        className={`category-button ${!selectedCategory ? 'active' : ''}`}
                        onClick={() => handleCategoryClick(null)}
                    >
                        Tüm Ürünler
                    </button>
                    {categories.map(category => (
                        <button
                            key={category.category_id}
                            className={`category-button ${selectedCategory === category.category_id ? 'active' : ''}`}
                            onClick={() => handleCategoryClick(category)}
                        >
                            {category.category_name}
                        </button>
                    ))}
                </div>
            </div>
            <div className="product-grid">
                {products.map((product) => (
                    <ProductCard key={product.product_id} product={product} />
                ))}
            </div>
            <Footer />
        </div>
    );
};

export default MainPage;