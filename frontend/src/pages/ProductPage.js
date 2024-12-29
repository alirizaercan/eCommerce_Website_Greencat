import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import Header from '../components/Header';
import '../styles/ProductPage.css';

const ProductPage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const location = useLocation();

  const handleSearch = (searchResults) => {
    setProducts(searchResults);
  };

  return (
    <div className="product-page">
      <Header onSearch={handleSearch} />
      <div className="product-list-container">
        {loading ? (
          <div className="loading">Yükleniyor...</div>
        ) : products.length > 0 ? (
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard key={product.product_id} product={product} />
            ))}
          </div>
        ) : (
          <div className="no-results">Ürün bulunamadı.</div>
        )}
      </div>
    </div>
  );
};

export default ProductPage;