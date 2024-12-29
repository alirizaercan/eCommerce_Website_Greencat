import React from "react";
import PropTypes from "prop-types";
import { useNavigate } from 'react-router-dom';
import "../styles/ProductCard.css";
import { useAuth } from '../services/AuthContext';
import { useCart } from '../services/CartContext';

const ProductCard = ({ product }) => {
  const { isLoggedIn, customerInfo } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const discountedPrice = product.discount 
    ? parseFloat(product.price) * (1 - parseFloat(product.discount.discount_percentage)/100) 
    : parseFloat(product.price);

  const taxAmount = parseFloat(product.tax);
  const finalPrice = discountedPrice + taxAmount;

  const handleAddToCart = async () => {
    if (!isLoggedIn || !customerInfo.customerId) {
      navigate('/login');
      return;
    }
  
    try {
      const success = await addToCart(product.product_id);
      if (success) {
        // Show success notification
        console.log('Item added to cart successfully');
      } else {
        // Show error notification
        console.error('Failed to add item to cart');
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img src={product.image_url} alt={product.product_name} className="product-image" />
        {product.discount && (
          <div className="discount-badge">
            %{product.discount.discount_percentage} İndirim
          </div>
        )}
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.product_name}</h3>
        <p className="product-category">{product.category?.category_name}</p>
        <p className="product-description">{product.product_description}</p>
        
        <div className="product-rating">
          <span className="stars">{'★'.repeat(Math.round(product.rating))}</span>
          <span className="review-count">({product.review_count} değerlendirme)</span>
        </div>

        <div className="product-price-container">
          {product.discount ? (
            <>
              <span className="original-price">{product.price} TL</span>
              <span className="discounted-price">{finalPrice.toFixed(2)} TL</span>
              <span className="tax-info">(KDV Dahil)</span>
            </>
          ) : (
            <>
              <span className="price">{finalPrice.toFixed(2)} TL</span>
              <span className="tax-info">(KDV Dahil)</span>
            </>
          )}
        </div>

        <button 
          className="add-to-cart-btn"
          onClick={handleAddToCart}
        >
          Sepete Ekle
        </button>
      </div>
    </div>
  );
};

ProductCard.propTypes = {
  product: PropTypes.shape({
    product_id: PropTypes.number.isRequired,
    product_name: PropTypes.string.isRequired,
    product_description: PropTypes.string,
    price: PropTypes.string.isRequired,
    tax: PropTypes.string.isRequired,
    rating: PropTypes.number.isRequired,
    review_count: PropTypes.number.isRequired,
    image_url: PropTypes.string,
    category: PropTypes.shape({
      category_name: PropTypes.string.isRequired,
    }),
    discount: PropTypes.shape({
      discount_percentage: PropTypes.string.isRequired,
    }),
  }).isRequired
};

export default ProductCard;