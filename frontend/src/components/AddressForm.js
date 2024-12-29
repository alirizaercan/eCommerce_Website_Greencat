import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import { addressApi } from '../services/addressApi';
import PropTypes from 'prop-types';
import '../styles/AddressForm.css';

const AddressForm = ({ onSuccess }) => {
  const navigate = useNavigate();
  const { customerInfo } = useAuth();
  
  const [formData, setFormData] = useState({
    address_line1: '',
    address_line2: '',
    city: '',
    postal_code: '',
    phone_number: '',
    address_type: 'HOME',
    country: 'Türkiye'
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validatePhoneNumber = (phone) => {
    return /^(05)[0-9][0-9][1-9]([0-9]){6}$/.test(phone);
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.address_line1?.trim()) {
      newErrors.address_line1 = 'Adres alanı zorunludur';
    }
    
    if (!formData.city?.trim()) {
      newErrors.city = 'Şehir alanı zorunludur';
    }
    
    if (!formData.address_line2?.trim()) {
      newErrors.address_line2 = 'İlçe alanı zorunludur';
    }
    
    if (!formData.postal_code?.trim()) {
      newErrors.postal_code = 'Posta kodu zorunludur';
    } else if (!/^\d{5}$/.test(formData.postal_code)) {
      newErrors.postal_code = 'Geçerli bir posta kodu giriniz (5 haneli)';
    }
    
    if (!formData.phone_number) {
      newErrors.phone_number = 'Telefon numarası zorunludur';
    } else if (!validatePhoneNumber(formData.phone_number)) {
      newErrors.phone_number = 'Geçerli bir telefon numarası giriniz (05XX XXX XX XX)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field) => (e) => {
    const value = e.target.value;
    setFormData((prev) => ({
      ...prev,
      [field]: value
    }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const result = await addressApi.createAddress(customerInfo.customerId, formData);
      
      if (result.success) {
        if (onSuccess) {
          onSuccess(result.address);
        }
        navigate('/checkout');
      } else {
        throw new Error(result.error || "Adres kaydedilirken bir hata oluştu");
      }
    } catch (error) {
      setErrors(prev => ({
        ...prev,
        submit: error.message || "Bir hata oluştu. Lütfen tekrar deneyiniz."
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="address-form-container">
      <form onSubmit={handleSubmit} className="address-form">
        <h2>Yeni Adres Ekle</h2>

        <div className="form-row">
          <div className="form-group">
            <label>Adres Tipi</label>
            <select
              value={formData.addressType}
              onChange={handleInputChange('addressType')}
            >
              <option value="HOME">Ev</option>
              <option value="WORK">İş</option>
              <option value="OTHER">Diğer</option>
            </select>
          </div>

          <div className="form-group">
            <label>Telefon*</label>
            <input
              type="tel"
              value={formData.phone_number}
              onChange={handleInputChange('phone_number')}
              placeholder="05XX XXX XX XX"
              className={errors.phone_number ? 'error' : ''}
            />
            {errors.phone_number && <span className="error-text">{errors.phone_number}</span>}
          </div>
        </div>

        <div className="form-group">
          <label>Açık Adres*</label>
          <input
            type="text"
            value={formData.address_line1}
            onChange={handleInputChange('address_line1')}
            placeholder="Sokak, Mahalle, Bina No, Daire No"
            className={errors.address_line1 ? 'error' : ''}
          />
          {errors.address_line1 && <span className="error-text">{errors.address_line1}</span>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>İlçe*</label>
            <input
              type="text"
              value={formData.address_line2}
              onChange={handleInputChange('address_line2')}
              className={errors.address_line2 ? 'error' : ''}
            />
            {errors.address_line2 && <span className="error-text">{errors.address_line2}</span>}
          </div>

          <div className="form-group">
            <label>Şehir*</label>
            <input
              type="text"
              value={formData.city}
              onChange={handleInputChange('city')}
              className={errors.city ? 'error' : ''}
            />
            {errors.city && <span className="error-text">{errors.city}</span>}
          </div>
        </div>

        <div className="form-group">
          <label>Posta Kodu*</label>
          <input
            type="text"
            value={formData.postal_code}
            onChange={handleInputChange('postal_code')}
            placeholder="XXXXX"
            maxLength={5}
            className={errors.postal_code ? 'error' : ''}
          />
          {errors.postal_code && <span className="error-text">{errors.postal_code}</span>}
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="button secondary"
            onClick={() => navigate('/checkout')}
            disabled={loading}
          >
            İptal
          </button>
          <button
            type="submit"
            className="button primary"
            disabled={loading}
          >
            {loading ? 'Kaydediliyor...' : 'Adresi Kaydet'}
          </button>
        </div>
      </form>
    </div>
  );
};

AddressForm.propTypes = {
  onSuccess: PropTypes.func
};

export default AddressForm;