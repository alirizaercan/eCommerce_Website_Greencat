import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCustomerById } from '../services/auth';
import { createSession } from '../services/sessionApi';
import CartView from '../components/CartView';
import Header from '../components/Header';
import '../styles/CartPage.css';

const CartPage = () => {
  const [customerFirstName, setCustomerFirstName] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const initializeCart = async () => {
      const customerId = localStorage.getItem('customerId');
      let currentSessionId = localStorage.getItem('sessionId');
  
      if (!customerId) {
          navigate('/login');
          return;
      }
  
      try {
          setLoading(true);
          
          const customerData = await getCustomerById(customerId);
          if (customerData?.first_name) {
              setCustomerFirstName(customerData.first_name);
          }
  
          if (!currentSessionId) {
              const sessionResponse = await createSession({ 
                  customer_id: customerId,
                  total: 0
              });
              
              if (sessionResponse?.session?.session_id) {
                  currentSessionId = sessionResponse.session.session_id;
                  localStorage.setItem('sessionId', currentSessionId);
              } else {
                  throw new Error('Oturum oluşturulamadı');
              }
          }
  
          setSessionId(currentSessionId);
          setError(null);
  
      } catch (err) {
          console.error('Sepet başlatma hatası:', err);
          localStorage.removeItem('sessionId');
          setError('Sepet yüklenemedi. Lütfen tekrar deneyin.');
      } finally {
          setLoading(false);
      }
  };

    initializeCart();
  }, [navigate]);

  if (loading) {
    return <div className="cart-page-loading">Sepetiniz yükleniyor...</div>;
  }

  if (error) {
    return <div className="cart-page-error">{error}</div>;
  }

  return (
    <div className="cart-page-container">
      <Header customerFirstName={customerFirstName} />
      <div className="cart-page">
        <h1 className="main-header">
          {customerFirstName ? `Merhaba, ${customerFirstName}!` : 'Sepetiniz'}
        </h1>
        {sessionId && <CartView sessionId={sessionId} />}
      </div>
    </div>
  );
};

export default CartPage;