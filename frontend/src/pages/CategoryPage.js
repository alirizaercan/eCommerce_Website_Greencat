import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { categoryApi } from '../services/categoryApi';
import ProductCard from '../components/ProductCard';
import '../styles/MainPage.css';

const CategoryPage = () => {
    const { slug } = useParams();
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);
    const [category, setCategory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const categories = await categoryApi.getAllCategories();
                const matchedCategory = categories.find(
                    cat => cat.category_name.toLowerCase().replace(/\s+/g, '-') === slug
                );

                if (!matchedCategory) {
                    navigate('/');
                    return;
                }

                setCategory(matchedCategory);
                const categoryProducts = await categoryApi.getCategoryProducts(matchedCategory.category_id);
                setProducts(categoryProducts);
            } catch (error) {
                console.error('Kategori bilgileri yüklenirken hata:', error);
                setError('Ürünler yüklenemedi');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [slug, navigate]);

    if (loading) return <div className="loading">Yükleniyor...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="main-page">
            <Header />
            <div className="category-page">
                <h1 className="category-title">{category?.category_name}</h1>
                <div className="product-grid">
                    {products.map((product) => (
                        <ProductCard key={product.product_id} product={product} />
                    ))}
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default CategoryPage;