import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import successIcon from '../assets/images/success_icon.png';
import '../styles/PaymentSuccess.css';

const PaymentSuccess = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { customerInfo } = useAuth();
  const { orderId } = location.state || {};

  useEffect(() => {
    if (!customerInfo?.customerId) {
      navigate('/login');
      return;
    }

    const timer = setTimeout(() => {
      navigate('/orders', { 
        state: { customerId: customerInfo.customerId } 
      });
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate, customerInfo]);

  return (
    <div className="payment-success-container">
      <div className="success-card">
        <img src={successIcon} alt="Başarılı" className="success-icon" />
        <h1>Ödeme Başarılı!</h1>
        <p>Siparişiniz onaylandı.</p>
        {orderId && <p className="order-id">Sipariş Numarası: {orderId}</p>}
        <p className="redirect-text">Siparişler sayfasına yönlendiriliyorsunuz...</p>
      </div>
    </div>
  );
};

export default PaymentSuccess;