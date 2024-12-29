import React from "react";
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import "../styles/CustomerPage.css";

const CustomerPage = () => {
  const { isLoggedIn, customerInfo } = useAuth();
  const navigate = useNavigate();

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="customer-page">
      <div className="customer-header">
        <h1>Profilim</h1>
        <p>Hoş geldiniz, {customerInfo.firstName} {customerInfo.lastName}!</p>
      </div>

      <div className="customer-content">
        <div className="customer-section">
          <h2>Kişisel Bilgiler</h2>
          <div className="info-box">
            <p><strong>Ad Soyad:</strong> {customerInfo.firstName} {customerInfo.lastName}</p>
            <p><strong>Müşteri No:</strong> {customerInfo.customerId}</p>
          </div>
        </div>

        <div className="customer-section">
          <h2>Adres Yönetimi</h2>
          <div className="action-box">
            <p>Teslimat adresi ekleyin</p>
            <button 
              className="address-btn"
              onClick={() => navigate('/address/new')}
            >
              Adres Ekle
            </button>
          </div>
        </div>

        <div className="customer-section">
          <h2>Sipariş Geçmişi</h2>
          <div className="action-box">
            <p>Geçmiş siparişlerinizi görüntüleyin</p>
            <button 
              className="order-btn"
              onClick={() => navigate('/orders')}
            >
              Siparişleri Görüntüle
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerPage;