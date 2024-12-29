import React, { useState, useEffect } from 'react';
import { orderApi } from '../services/orderApi';
import { carrierApi } from '../services/carrierApi';
import { useAuth } from '../services/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/OrderList.css';

const OrderList = () => {
    const { customerInfo } = useAuth();
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const [carriers, setCarriers] = useState({});

    useEffect(() => {
        const fetchOrders = async () => {
            if (!customerInfo?.customerId) {
                setError('Siparişleri görüntülemek için lütfen giriş yapın');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const data = await orderApi.getCustomerOrders(customerInfo.customerId);
                const processedOrders = data.map(order => ({
                    ...order,
                    items: order.items || []
                }));
                setOrders(processedOrders);
                setError(null);
            } catch (err) {
                console.error('Siparişler yüklenirken hata:', err);
                setError(err.response?.data?.error || 'Siparişler yüklenemedi');
                setOrders([]);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, [customerInfo]);

    useEffect(() => {
        const fetchCarriers = async () => {
            const carrierData = {};
            for (const order of orders) {
                try {
                    const response = await carrierApi.getOrderCarrier(order.order_id);
                    carrierData[order.order_id] = response.carrier_name;
                } catch (err) {
                    console.error(`Kargo bilgisi alınamadı, Sipariş No: ${order.order_id}:`, err);
                }
            }
            setCarriers(carrierData);
        };

        if (orders.length > 0) {
            fetchCarriers();
        }
    }, [orders]);

    if (loading) return <div className="order-list-loading">Siparişler yükleniyor...</div>;
    if (error) return <div className="order-list-error">{error}</div>;
    if (orders.length === 0) return <div className="order-list-empty">Sipariş bulunamadı</div>;

    return (
        <div className="order-list-container">
            <div className="top-navigation">
                <button className="main-page-button-top" onClick={() => navigate('/')}>
                    Ana Sayfaya Dön
                </button>
            </div>
            <div className="order-list">
                <h2>Sipariş Geçmişi</h2>
                <div className="orders-container">
                    {orders.map(order => (
                        <div key={order.order_id} className="order-card">
                            <div className="order-header">
                                <div className="order-info">
                                    <h3 className="order-id">Sipariş #{order.order_id}</h3>
                                    <span className={`status ${order.order_status.toLowerCase()}`}>
                                        {order.order_status}
                                    </span>
                                    <h3 className="carrier-info">
                                        <span className="carrier-label">Kargo Bilgisi:</span>
                                        <span className="carrier-name">
                                            {carriers[order.order_id] || 'Atanıyor...'}
                                        </span>
                                    </h3>
                                </div>
                                <div className="order-summary">
                                    <p className="order-date">
                                        <strong>Tarih:</strong> {new Date(order.created_at).toLocaleString()}
                                    </p>
                                    <p className="order-total">
                                        <strong>Toplam:</strong> {parseFloat(order.total).toFixed(2)} TL
                                    </p>
                                    <p className="order-tax">
                                        <strong>KDV:</strong> {parseFloat(order.tax).toFixed(2)} TL
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default OrderList;