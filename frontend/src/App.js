import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CategoryPage from './pages/CategoryPage';
import CartPage from './pages/CartPage';
import OrderList from './components/OrderList';
import SessionSummary from './components/SessionSummary';
import PaymentForm from './components/PaymentForm';
import CustomerPage from './pages/CustomerPage';
import { AuthProvider } from './services/AuthContext';
import AddressForm from './components/AddressForm';
import { CartProvider } from './services/CartContext';
import CheckoutPage from './pages/CheckoutPage';
import PaymentSuccess from './components/PaymentSuccess';
import ProductPage from './pages/ProductPage';
import AdminPage from './pages/AdminPage';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/address/new" element={<AddressForm />} />
            <Route path="/category/:slug" element={<CategoryPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/orders" element={<OrderList />} />
            <Route path="/sessions/:sessionId" element={<SessionSummary />} />
            <Route path="/payments/:orderId" element={<PaymentForm />} />
            <Route path="/profile" element={<CustomerPage />} /> {/* Yeni rota */}
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/payment-success" element={<PaymentSuccess />} />
            <Route path="/products" element={<ProductPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;