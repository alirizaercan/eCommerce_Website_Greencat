import React, { createContext, useState, useContext, useEffect } from 'react';
import { addItemToCart, getCartItems, deleteCartItem, updateCartItem } from './cartApi';
import { createSession } from './sessionApi';
import { useAuth } from './AuthContext';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId'));
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const { isLoggedIn, customerInfo } = useAuth();

  const addToCart = async (productId) => {
    try {
      if (!sessionId) {
        const response = await createSession({
          customer_id: customerInfo.customerId,
          total: 0
        });
        
        if (!response?.session?.session_id) {
          throw new Error('Failed to create session');
        }
        
        setSessionId(response.session.session_id);
        localStorage.setItem('sessionId', response.session.session_id);
      }
  
      const newItem = await addItemToCart(sessionId, productId, 1);
      if (newItem) {
        await refreshCart();
        return true;
      }
      return false;
    } catch (error) {
      if (error.response?.status === 500) {
        try {
          await createNewSession();
          return addToCart(productId);
        } catch (retryError) {
          console.error('Retry failed:', retryError);
          return false;
        }
      }
      console.error('Error adding to cart:', error);
      return false;
    }
  };

  const removeFromCart = async (cartItemId) => {
    try {
      const result = await deleteCartItem(cartItemId);
      if (result.success) {
        await refreshCart();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Remove from cart error:', error);
      return false;
    }
  };

  const createNewSession = async () => {
    try {
      if (!customerInfo?.customerId) {
        throw new Error('No customer ID available');
      }

      const response = await createSession({
        customer_id: customerInfo.customerId,
        total: 0
      });
      
      if (response?.session?.session_id) {
        setSessionId(response.session.session_id);
        localStorage.setItem('sessionId', response.session.session_id);
        return response.session.session_id;
      }
      throw new Error('Failed to create new session');
    } catch (error) {
      console.error('Failed to create new session:', error);
      throw error;
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    try {
      setLoading(true);
      await updateCartItem(itemId, quantity);
      await refreshCart();
      return true;
    } catch (error) {
      console.error('Update quantity error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const refreshCart = async () => {
    if (!sessionId) return;
    try {
      const items = await getCartItems(sessionId);
      setCartItems(items || []);
      setCartData({
        items,
        total: items.reduce((sum, item) => sum + item.subtotal, 0),
        tax: items.reduce((sum, item) => sum + item.tax, 0),
        subtotal: items.reduce((sum, item) => sum + item.subtotal, 0)
      });
    } catch (error) {
      console.error('Refresh cart error:', error);
    }
  };

  useEffect(() => {
    const initSession = async () => {
      try {
        if (isLoggedIn && customerInfo?.customerId) {
          const existingSessionId = localStorage.getItem('sessionId');
          
          if (existingSessionId) {
            try {
              await getCartItems(existingSessionId);
              setSessionId(existingSessionId);
              await refreshCart();
            } catch (error) {
              localStorage.removeItem('sessionId');
              await createNewSession();
            }
          } else {
            await createNewSession();
          }
        }
      } catch (error) {
        console.error('Session initialization error:', error);
      } finally {
        setIsInitializing(false);
      }
    };

    initSession();
  }, [isLoggedIn, customerInfo]);

  const value = {
    cartItems,
    cartData,
    sessionId, // Add sessionId to context
    loading,
    addToCart,
    updateQuantity,
    refreshCart,
    setSessionId,
    removeFromCart,
    updateQuantity
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);