import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [customerInfo, setCustomerInfo] = useState({
    customerId: null,
    firstName: null,
    lastName: null,
    email: null,
    username: null,
    sessionId: null
  });

  const updateAuthState = (loginData) => {
    if (loginData && loginData.customer_id) {
      setIsLoggedIn(true);
      setCustomerInfo({
        customerId: loginData.customer_id,
        firstName: loginData.first_name,
        lastName: loginData.last_name,
        email: loginData.email,
        username: loginData.username,
        sessionId: loginData.session_id
      });

      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('customerId', loginData.customer_id);
      localStorage.setItem('customerFirstName', loginData.first_name);
      localStorage.setItem('customerLastName', loginData.last_name);
      localStorage.setItem('sessionId', loginData.session_id);
      localStorage.setItem('email', loginData.email);
      localStorage.setItem('username', loginData.username);
    }
  };

  const clearAuthState = () => {
    setIsLoggedIn(false);
    setCustomerInfo({
      customerId: null,
      firstName: null,
      lastName: null,
      email: null,
      username: null,
      sessionId: null
    });
    
    localStorage.clear();
  };

  useEffect(() => {
    const checkLoginStatus = () => {
      const storedLoginState = localStorage.getItem('isLoggedIn') === 'true';
      const customerId = localStorage.getItem('customerId');
      const sessionId = localStorage.getItem('sessionId');

      if (storedLoginState && customerId && sessionId) {
        setIsLoggedIn(true);
        setCustomerInfo({
          customerId,
          firstName: localStorage.getItem('customerFirstName'),
          lastName: localStorage.getItem('customerLastName'),
          email: localStorage.getItem('email'),
          username: localStorage.getItem('username'),
          sessionId
        });
      } else {
        clearAuthState();
      }
    };

    checkLoginStatus();
    window.addEventListener('storage', checkLoginStatus);
    return () => window.removeEventListener('storage', checkLoginStatus);
  }, []);

  return (
    <AuthContext.Provider value={{
      isLoggedIn,
      customerInfo,
      updateAuthState,
      clearAuthState,
      setIsLoggedIn
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);