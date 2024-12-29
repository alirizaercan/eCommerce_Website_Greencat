import React, { useState } from "react";
import PropTypes from 'prop-types';
import { useNavigate } from "react-router-dom";
import { logoutCustomer } from "../services/auth";
import {searchProducts} from "../services/productApi";
import { useAuth } from "../services/AuthContext";
import greenCatIcon from "../assets/images/green_cat_icon.png";
import loginIcon from "../assets/images/login_icon.png";
import shoppingCartIcon from "../assets/images/shopping_cart_icon.png";
import logoutIcon from "../assets/images/logout_icon.png";
import "../styles/Header.css";

const Header = ({ onSearch, cartItemCount = 0 }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate();
  const { isLoggedIn, customerInfo, clearAuthState } = useAuth();

  const handleSearch = async () => {
    if (searchTerm.trim()) {
      setIsSearching(true);
      try {
        const products = await searchProducts(searchTerm.trim());
        onSearch(products); // Pass results to parent component
        navigate('/products', { state: { searchResults: products } });
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setIsSearching(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Update search input
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleLogout = async () => {
    try {
      await logoutCustomer();
      clearAuthState();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const handleProfileClick = () => {
    if (isLoggedIn) {
      navigate("/profile");
    } else {
      navigate("/login");
    }
  };

  return (
    <header className="header">
      <div className="header-logo" onClick={() => navigate("/")}>
        <img src={greenCatIcon} alt="Green Cat Logo" className="header-logo-icon" />
      </div>

      <div className="header-search">
        <input
          type="text"
          placeholder="Ürün ara..."
          value={searchTerm}
          onChange={handleSearchChange}
          onKeyPress={handleKeyPress}
          className="search-box"
          disabled={isSearching}
        />
        <button 
          className="search-button" 
          onClick={handleSearch}
          disabled={isSearching || !searchTerm.trim()}
        >
          {isSearching ? 'Aranıyor...' : 'Ara'}
        </button>
      </div>

      <div className="header-actions">
        {isLoggedIn ? (
          <div className="header-profile-container">
            <button className="user-welcome" onClick={handleProfileClick}>
              Merhaba, {customerInfo?.firstName || ''}
            </button>
            <img
              src={logoutIcon}
              alt="Logout Icon"
              className="header-action-icon logout-icon"
              onClick={handleLogout}
            />
          </div>
        ) : (
          <div className="header-login" onClick={() => navigate("/login")}>
            <img src={loginIcon} alt="Login Icon" className="header-action-icon" />
            <span>Login</span>
          </div>
        )}

        <div className="header-cart" onClick={() => navigate("/cart")}>
          <div className="cart-icon-container">
            <img src={shoppingCartIcon} alt="Sepet" className="header-action-icon" />
            {cartItemCount > 0 && <span className="cart-badge">{cartItemCount}</span>}
          </div>
          <span>Sepet</span>
        </div>
      </div>
    </header>
  );
};

Header.propTypes = {
  onSearch: PropTypes.func.isRequired,
  cartItemCount: PropTypes.number
};

Header.defaultProps = {
  cartItemCount: 0
};

export default Header;