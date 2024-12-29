import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import { useCart } from '../services/CartContext';
import { addressApi } from '../services/addressApi';
import { validateCheckout, processCheckout, createAddress } from '../services/checkoutApi';
import PaymentForm from '../components/PaymentForm';
import PropTypes from 'prop-types';
import '../styles/CheckoutPage.css';

// Component definitions
const CheckoutSteps = ({ currentStep }) => (
  <div className="checkout-steps">
    <div className={`step ${currentStep === 'address' ? 'active' : currentStep === 'payment' ? 'completed' : ''}`}>
      <span className="step-number">1</span>
      <span className="step-title">Teslimat Adresi</span>
    </div>
    <div className={`step ${currentStep === 'payment' ? 'active' : ''}`}>
      <span className="step-number">2</span>
      <span className="step-title">Ödeme</span>
    </div>
  </div>
);

const OrderSummary = ({ cartData }) => (
  <div className="order-summary">
    <h3>Sipariş Özeti</h3>
    <div className="summary-items">
      {cartData?.items?.map(item => (
        <div key={item.id} className="summary-item">
          <span>{item.product.product_name} × {item.quantity}</span>
          <span>{Number(item.subtotal).toFixed(2)} TL</span>
        </div>
      ))}
    </div>
    <div className="summary-totals">
      <div className="summary-row">
        <span>Ara Toplam</span>
        <span>{Number(cartData?.subtotal).toFixed(2)} TL</span>
      </div>
      <div className="summary-row">
        <span>KDV</span>
        <span>{Number(cartData?.tax).toFixed(2)} TL</span>
      </div>
      <div className="summary-row total">
        <span>Toplam</span>
        <span>{Number(cartData?.total).toFixed(2)} TL</span>
      </div>
    </div>
  </div>
);

const AddressSelection = ({ addresses, selectedAddressId, onSelect, onAddNew }) => (
  <div className="address-selection">
    <div className="section-header">
      <h2>Teslimat Adresi Seçin</h2>
      <button className="add-new-btn" onClick={onAddNew}>+ Yeni Adres Ekle</button>
    </div>
    <div className="addresses-grid">
      {addresses.map(address => (
        <div 
          key={address.address_id}
          className={`address-card ${selectedAddressId === address.address_id ? 'selected' : ''}`}
          onClick={() => onSelect(address.address_id)}
        >
          <div className="address-card-content">
            <div className="address-type">{address.address_type || 'Ev'}</div>
            <p className="address-title">{address.title || 'Adres'}</p>
            <p className="address-street">{address.address_line1}</p>
            <p className="address-district">{address.district}</p>
            <p className="address-city">{address.city}</p>
            <p className="address-postal">{address.postal_code}</p>
          </div>
          {selectedAddressId === address.address_id && (
            <div className="selected-indicator">✓</div>
          )}
        </div>
      ))}
    </div>
  </div>
);

// Main component
const CheckoutPage = () => {
  const navigate = useNavigate();
  const { isLoggedIn, customerInfo } = useAuth();
  const { cartData: contextCartData, sessionId } = useCart();

  const [step, setStep] = useState('address');
  const [addresses, setAddresses] = useState([]);
  const [selectedAddressId, setSelectedAddressId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cartData, setCartData] = useState(null);

  // Effects
  useEffect(() => {
    const initCheckout = async () => {
      if (!customerInfo?.customerId || !sessionId) {
        navigate('/login');
        return;
      }

      try {
        setLoading(true);
        const result = await validateCheckout(customerInfo.customerId, sessionId);
        
        if (!result.success || !result.has_items) {
          navigate('/cart');
          return;
        }

        setAddresses(result.addresses || []);
        setSelectedAddressId(result.addresses?.[0]?.address_id || null);
        setCartData(result.summary || contextCartData);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    initCheckout();
  }, [customerInfo, sessionId, contextCartData, navigate]);

  // Handlers
  const handleAddressSubmit = async (addressData) => {
    try {
        setLoading(true);
        const result = await addressApi.createAddress({
            ...addressData,
            customer_id: customerInfo.customerId
        });
        
        if (result.success) {
            setAddresses([...addresses, result.address]);
            setSelectedAddressId(result.address.address_id);
            setStep('address');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        setError(error.message);
    } finally {
        setLoading(false);
    }
};

  const handlePaymentSubmit = async (paymentData) => {
    try {
      setLoading(true);
      
      if (!paymentData?.cardNumber || !cartData?.total) {
        throw new Error('Invalid payment or cart data');
      }

      const result = await processCheckout({
        customer_id: customerInfo.customerId,
        session_id: sessionId,
        address_id: selectedAddressId,
        payment: {
          amount: Number(cartData.total),
          card_number: String(paymentData.cardNumber).replace(/-/g, ''),
          card_holder: paymentData.cardHolder || '',
          expiry_date: paymentData.expiryDate || '',
          cvv: paymentData.cvv || ''
        }
      });

      if (result.success) {
        navigate('/payment-success', { 
          state: { orderId: result.order?.order_id }
        });
      } else {
        throw new Error(result.error || 'Checkout failed');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return (
    <div className="checkout-error">
      <p>{error}</p>
      <button onClick={() => navigate('/cart')}>Sepete Dön</button>
    </div>
  );

  return (
    <div className="checkout-container">
      <CheckoutSteps currentStep={step} />
      <div className="checkout-content">
        <div className="checkout-main">
          {step === 'address' && (
            <AddressSelection
              addresses={addresses}
              selectedAddressId={selectedAddressId}
              onSelect={setSelectedAddressId}
              onAddNew={() => navigate('/address/new')}
            />
          )}
          {step === 'payment' && (
            <PaymentForm 
              onSubmit={handlePaymentSubmit}
              amount={cartData?.total}
              selectedAddressId={selectedAddressId}
            />
          )}
          <div className="checkout-actions">
            {step === 'address' && (
              <button
                className="primary-button"
                onClick={() => setStep('payment')}
                disabled={!selectedAddressId}
              >
                Ödemeye Geç
              </button>
            )}
          </div>
        </div>
        <OrderSummary cartData={cartData} />
      </div>
    </div>
  );
};

// PropTypes
CheckoutSteps.propTypes = {
  currentStep: PropTypes.oneOf(['address', 'payment']).isRequired
};

OrderSummary.propTypes = {
  cartData: PropTypes.shape({
    items: PropTypes.array,
    subtotal: PropTypes.number,
    tax: PropTypes.number,
    total: PropTypes.number
  })
};

AddressSelection.propTypes = {
  addresses: PropTypes.arrayOf(
    PropTypes.shape({
      address_id: PropTypes.number.isRequired,
      address_type: PropTypes.string,
      title: PropTypes.string,
      address_line1: PropTypes.string.isRequired,
      district: PropTypes.string,
      city: PropTypes.string.isRequired,
      postal_code: PropTypes.string.isRequired
    })
  ).isRequired,
  selectedAddressId: PropTypes.number,
  onSelect: PropTypes.func.isRequired,
  onAddNew: PropTypes.func.isRequired
};

export default CheckoutPage;