import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { processPayment } from '../services/paymentApi';
import '../styles/PaymentForm.css';

const PaymentForm = ({ onSubmit, amount, selectedAddressId }) => {
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [formData, setFormData] = useState({
    cardNumber: '',
    cardHolder: '',
    expiryDate: '',
    cvv: '',
    cardType: ''
  });
  const [formErrors, setFormErrors] = useState({});

  const formattedAmount = Number(amount || 0).toFixed(2);

  const validateForm = () => {
    const errors = {};
    
    if (!formData.cardNumber) {
      errors.cardNumber = 'Kart numarası gerekli';
    } else if (formData.cardNumber.replace(/-/g, '').length !== 16) {
      errors.cardNumber = 'Kart numarası 16 haneli olmalı';
    }

    if (!formData.cardHolder) {
      errors.cardHolder = 'Kart sahibi adı gerekli';
    }

    if (!formData.expiryDate) {
      errors.expiryDate = 'Son kullanma tarihi gerekli';
    } else if (!/^\d{2}\/\d{2}$/.test(formData.expiryDate)) {
      errors.expiryDate = 'Geçersiz son kullanma tarihi formatı';
    }

    if (!formData.cvv) {
      errors.cvv = 'CVV gerekli';
    } else if (!/^\d{3}$/.test(formData.cvv)) {
      errors.cvv = 'CVV 3 haneli olmalı';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const formatCardNumber = (value) => {
    if (!value) return '';
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    return parts.length ? parts.join('-') : value;
  };

  const formatExpiryDate = (value) => {
    if (!value) return '';
    const cleanValue = value.replace(/[^\d]/g, '');
    if (cleanValue.length >= 2) {
      return `${cleanValue.slice(0, 2)}/${cleanValue.slice(2, 4)}`;
    }
    return cleanValue;
  };

  const determineCardType = (number) => {
    if (!number) return '';
    const cleanNumber = number.replace(/-/g, '').trim();
    if (!cleanNumber) return '';
    
    const lastDigit = parseInt(cleanNumber.slice(-1));
    if (isNaN(lastDigit)) return '';
    
    if (lastDigit >= 0 && lastDigit <= 3) return 'VISA';
    if (lastDigit >= 4 && lastDigit <= 6) return 'MASTERCARD';
    if (lastDigit >= 7 && lastDigit <= 9) return 'TROY';
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
  
    const paymentData = {
      cardNumber: formData.cardNumber || '',
      cardHolder: formData.cardHolder || '',
      expiryDate: formData.expiryDate || '',
      cvv: formData.cvv || '',
      cardType: formData.cardType || ''
    };
  
    try {
      await onSubmit(paymentData);
    } catch (error) {
      setFormErrors({ submit: error.message });
    }
  };

  const handleCardNumberChange = (e) => {
    const value = e.target.value;
    const formattedValue = formatCardNumber(value);
    const cardType = determineCardType(formattedValue);
    
    setFormData(prev => ({
      ...prev,
      cardNumber: formattedValue,
      cardType
    }));
  };

  if (showSuccess) {
    return (
      <div className="success-message">
        <h2>Ödeme Başarılı!</h2>
        <p>Siparişlerinize yönlendiriliyorsunuz...</p>
      </div>
    );
  }

  return (
    <div className="payment-form-container">
      <form onSubmit={handleSubmit} className="payment-form">
        <h2>Ödeme Bilgileri</h2>
        
        {formData.cardType && (
          <div className="card-type">Kart Türü: {formData.cardType}</div>
        )}
        
        <div className="form-group">
          <label>Kart Numarası</label>
          <input
            type="text"
            value={formData.cardNumber}
            onChange={handleCardNumberChange}
            maxLength="19"
            placeholder="1234-5678-9012-3456"
            required
          />
          {formErrors.cardNumber && (
            <div className="error-message">{formErrors.cardNumber}</div>
          )}
        </div>

        <div className="form-group">
          <label>Kart Sahibi Adı</label>
          <input
            type="text"
            value={formData.cardHolder}
            onChange={(e) => setFormData({...formData, cardHolder: e.target.value})}
            placeholder="Ad Soyad"
            required
          />
          {formErrors.cardHolder && (
            <div className="error-message">{formErrors.cardHolder}</div>
          )}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Son Kullanma Tarihi</label>
            <input
              type="text"
              value={formData.expiryDate}
              onChange={(e) => setFormData({...formData, expiryDate: formatExpiryDate(e.target.value)})}
              placeholder="AA/YY"
              maxLength="5"
              required
            />
            {formErrors.expiryDate && (
              <div className="error-message">{formErrors.expiryDate}</div>
            )}
          </div>

          <div className="form-group">
            <label>CVV</label>
            <input
              type="text"
              value={formData.cvv}
              onChange={(e) => setFormData({...formData, cvv: e.target.value.replace(/\D/g, '')})}
              placeholder="123"
              maxLength="3"
              required
            />
            {formErrors.cvv && (
              <div className="error-message">{formErrors.cvv}</div>
            )}
          </div>
        </div>

        {formErrors.submit && (
          <div className="error-message submit-error">{formErrors.submit}</div>
        )}

        <button 
          type="submit" 
          className="submit-button"
          disabled={isProcessing}
        >
          {isProcessing ? 'İşlem Yapılıyor...' : `${formattedAmount} TL Öde`}
        </button>
      </form>
    </div>
  );
};

export default PaymentForm;
