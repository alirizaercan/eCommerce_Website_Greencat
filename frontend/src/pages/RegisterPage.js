import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerCustomer } from "../services/auth";
import "../styles/RegisterPage.css";

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    phone_number: ""
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    // Ad-Soyad kontrolü
    if (formData.first_name.trim().length < 2) {
      newErrors.first_name = "Ad en az 2 karakter olmalıdır";
    }
    if (formData.last_name.trim().length < 2) {
      newErrors.last_name = "Soyad en az 2 karakter olmalıdır";
    }

    // Kullanıcı adı kontrolü
    if (formData.username.trim().length < 4) {
      newErrors.username = "Kullanıcı adı en az 4 karakter olmalıdır";
    }

    // Email formatı kontrolü
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = "Geçerli bir e-posta adresi giriniz";
    }

    // Şifre kompleksitesi kontrolü
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    if (!passwordRegex.test(formData.password)) {
      newErrors.password = "Şifre en az 8 karakter olmalı ve büyük harf, küçük harf ve rakam içermelidir";
    }

    // Telefon numarası formatı kontrolü
    const phoneRegex = /^\+?[\d\s-]{10,}$/;
    if (!phoneRegex.test(formData.phone_number)) {
      newErrors.phone_number = "Geçerli bir telefon numarası giriniz";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    // Input değiştiğinde ilgili error'u temizle
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: "" }));
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    if (!validateForm()) {
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await registerCustomer(formData);
      if (response.message === "Registration successful") {
        navigate("/login");
      } else {
        setErrors(prev => ({
          ...prev,
          general: response.message
        }));
      }
    } catch (error) {
      let errorMessage = "Kayıt sırasında bir hata oluştu";
      
      if (error.response?.data?.message) {
        // Backend'den gelen spesifik hata mesajı
        errorMessage = error.response.data.message;
      } else if (!navigator.onLine) {
        errorMessage = "Lütfen internet bağlantınızı kontrol edin";
      }
      
      setErrors(prev => ({
        ...prev,
        general: errorMessage
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-page">
      <h2>Kayıt Ol</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Ad"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        {errors.first_name && <div className="error">{errors.first_name}</div>}

        <input
          type="text"
          placeholder="Soyad"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />
        {errors.last_name && <div className="error">{errors.last_name}</div>}

        <input
          type="text"
          placeholder="Kullanıcı Adı"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        {errors.username && <div className="error">{errors.username}</div>}

        <input
          type="email"
          placeholder="E-posta"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        {errors.email && <div className="error">{errors.email}</div>}

        <input
          type="password"
          placeholder="Şifre"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {errors.password && <div className="error">{errors.password}</div>}

        <input
          type="tel"
          placeholder="Telefon Numarası"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          required
        />
        {errors.phone_number && <div className="error">{errors.phone_number}</div>}

        {errors.general && <div className="error general">{errors.general}</div>}
        
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Kaydediliyor..." : "Kayıt Ol"}
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;
