import React, { useState } from 'react';
import { adminApi } from '../services/adminApi';
import '../styles/AdminPage.css';

const GRAPH_OPTIONS = [
    { value: "Gelir Analizi", label: "Gelir Analizi" },
    { value: "Ürün Satışları", label: "Ürün Satışları" },
    { value: "Müşteri Aktivitesi", label: "Müşteri Aktivitesi" },
    { value: "Sipariş Durumu", label: "Sipariş Durumu" },
    { value: "Kategori Performansı", label: "Kategori Performansı" }
];

const AdminPage = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [adminData, setAdminData] = useState(null);
    const [loginForm, setLoginForm] = useState({ username: '', password: '' });
    const [graphType, setGraphType] = useState('');
    const [dateRange, setDateRange] = useState({ start: '', end: '' });
    const [graphPath, setGraphPath] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const response = await adminApi.login(loginForm);
            if (response.success) {
                setIsLoggedIn(true);
                setAdminData(response.admin);
            } else {
                setError(response.message || 'Giriş başarısız');
            }
        } catch (error) {
            setError(error.message || 'Giriş başarısız');
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerateGraph = async () => {
        if (!graphType || !dateRange.start || !dateRange.end) {
            setError('Lütfen grafik türü ve tarih aralığı seçin');
            return;
        }
    
        setIsLoading(true);
        setError('');
        try {
            const response = await adminApi.generateGraph({
                graph_type: graphType,
                start_date: dateRange.start,
                end_date: dateRange.end
            });
    
            if (response.path) {
                const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
                setGraphPath(`${baseUrl}${response.path}?t=${new Date().getTime()}`);
            } else {
                setError('Grafik oluşturulamadı');
            }
        } catch (error) {
            setError(error.message || 'Grafik oluşturma hatası');
        } finally {
            setIsLoading(false);
        }
    };

    if (!isLoggedIn) {
        return (
            <div className="admin-login">
                <form onSubmit={handleLogin}>
                    <h2>Yönetici Girişi</h2>
                    {error && <div className="error-message">{error}</div>}
                    <input
                        type="text"
                        placeholder="Kullanıcı Adı"
                        value={loginForm.username}
                        onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                        disabled={isLoading}
                    />
                    <input
                        type="password"
                        placeholder="Şifre"
                        value={loginForm.password}
                        onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                        disabled={isLoading}
                    />
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
                    </button>
                </form>
            </div>
        );
    }

    return (
        <div className="admin-dashboard">
            <header className="dashboard-header">
                <h1>Yönetici Paneli</h1>
                <div className="admin-info">
                    <p>Hoşgeldiniz, {adminData?.username}</p>
                    <p>Yetki: {adminData?.type}</p>
                </div>
            </header>

            <div className="graph-controls">
                <select
                    value={graphType}
                    onChange={(e) => setGraphType(e.target.value)}
                    className="graph-type-select"
                >
                    <option value="">Grafik Türü Seçin</option>
                    {GRAPH_OPTIONS.map(option => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>

                <div className="date-inputs">
                    <input
                        type="date"
                        value={dateRange.start}
                        onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
                        className="date-input"
                    />
                    <input
                        type="date"
                        value={dateRange.end}
                        onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
                        className="date-input"
                    />
                </div>

                <button 
                    onClick={handleGenerateGraph}
                    disabled={isLoading || !graphType || !dateRange.start || !dateRange.end}
                    className="generate-button"
                >
                    {isLoading ? 'Oluşturuluyor...' : 'Grafik Oluştur'}
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="graph-display">
                {isLoading ? (
                    <div className="loading-spinner">Grafik oluşturuluyor...</div>
                ) : graphPath ? (
                    <img
                        src={graphPath}
                        alt="Oluşturulan Grafik"
                        className="graph-image"
                        onError={(e) => {
                            setError('Grafik yüklenirken hata oluştu');
                            e.target.style.display = 'none';
                        }}
                    />
                ) : (
                    <div className="no-graph">Parametre seçin ve grafik oluşturun</div>
                )}
            </div>
        </div>
    );
};

export default AdminPage;