import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../services/CartContext';
import { getCartItems, updateCartItem, deleteCartItem } from '../services/cartApi';
import '../styles/CartView.css';

const CartView = () => {
  const navigate = useNavigate();
  const { sessionId, removeFromCart } = useCart();
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCartData();
  }, [sessionId]);

  const fetchCartData = async () => {
    if (!sessionId) return;
    
    try {
      setLoading(true);
      const data = await getCartItems(sessionId);
      setCartData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load cart items');
      console.error('Cart loading error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuantity = async (cartItemId, quantity) => {
    if (quantity < 1) return;
    
    try {
      setLoading(true);
      await updateCartItem(cartItemId, quantity);
      await fetchCartData();
    } catch (err) {
      setError('Failed to update quantity');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteItem = async (cartItemId) => {
    try {
      setLoading(true);
      const success = await removeFromCart(cartItemId);
      
      if (success) {
        setCartData(prev => {
          const removedItem = prev.items.find(item => item.cart_item_id === cartItemId);
          const newSubtotal = prev.subtotal - (removedItem?.subtotal || 0);
          const newTaxTotal = prev.total_tax - (removedItem?.tax_amount || 0);
          const newTotal = newSubtotal + newTaxTotal;
          
          return {
            ...prev,
            items: prev.items.filter(item => item.cart_item_id !== cartItemId),
            total_items: prev.total_items - 1,
            subtotal: newSubtotal,
            total_tax: newTaxTotal,
            total: newTotal
          };
        });
      } else {
        setError('Ürün sepetten kaldırılamadı');
      }
    } catch (err) {
      console.error('Delete error:', err);
      setError('Ürün sepetten kaldırılamadı');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="cart-loading">Loading your cart...</div>;
  if (error) return <div className="cart-error">{error}</div>;
  if (!cartData?.items?.length) return <div className="cart-empty">Your cart is empty</div>;

  if (loading) return <div className="cart-loading">Sepetiniz yükleniyor...</div>;
  if (error) return <div className="cart-error">{error}</div>;
  if (!cartData?.items?.length) return <div className="cart-empty">Sepetiniz boş</div>;

  return (
    <div className="cart-container">
      <div className="cart-view">
        <h2 className="cart-title">Sepetim ({cartData.total_items} ürün)</h2>
        
        <div className="cart-content">
          <div className="cart-items">
            {cartData.items.map((item) => (
              <div key={item.cart_item_id} className="cart-item">
                <div className="item-image">
                  <img src={item.product.image_url} alt={item.product.product_name} />
                </div>
                <div className="item-details">
                  <h3>{item.product.product_name}</h3>
                  <p className="category">{item.product.category_name}</p>
                  <div className="price-details">
                    <p className="price">
                      {item.product.price.toFixed(2)} TL
                      {item.product.discount && (
                        <span className="discount">
                          %{item.product.discount.discount_percentage} İndirim
                        </span>
                      )}
                    </p>
                    <p className="tax">KDV: {item.tax_amount.toFixed(2)} TL</p>
                  </div>
                  <div className="quantity-controls">
                    <button 
                      onClick={() => handleUpdateQuantity(item.cart_item_id, item.quantity - 1)}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button 
                      onClick={() => handleUpdateQuantity(item.cart_item_id, item.quantity + 1)}
                    >
                      +
                    </button>
                  </div>
                  <p className="subtotal">
                    Ara Toplam: {item.subtotal.toFixed(2)} TL
                  </p>
                  <button 
                    className="remove-item"
                    onClick={() => handleDeleteItem(item.cart_item_id)}
                  >
                    Kaldır
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <h3>Sipariş Özeti</h3>
            <div className="summary-row">
              <span>Ara Toplam:</span>
              <span>{cartData.subtotal.toFixed(2)} TL</span>
            </div>
            <div className="summary-row">
              <span>KDV:</span>
              <span>{cartData.total_tax.toFixed(2)} TL</span>
            </div>
            <div className="summary-row total">
              <span>Toplam:</span>
              <span>{(cartData.subtotal + cartData.total_tax).toFixed(2)} TL</span>
            </div>
            <button className="checkout-button" onClick={() => navigate('/checkout')}>
              Alışverişi Tamamla
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartView;