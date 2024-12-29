import React, { useState } from "react";
import { registerCustomer, loginCustomer, getCustomerById, updateCustomer, deleteCustomer } from "../services/auth";

const AuthenticationPage = () => {
  const [formType, setFormType] = useState("login");
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    email: "",
    phone_number: ""
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formType === "login") {
      const response = await loginCustomer({
        username: formData.username,
        password: formData.password,
      });
      setMessage(response.message || "Giriş sırasında hata oluştu");
    } else {
      const response = await registerCustomer(formData);
      setMessage(response.message || "Kayıt sırasında hata oluştu");
    }
  };

  return (
    <div>
      <h1>{formType === "login" ? "Giriş Yap" : "Kayıt Ol"}</h1>
      <form onSubmit={handleSubmit}>
        {formType === "register" && (
          <>
            <input
              type="text"
              name="first_name"
              placeholder="Ad"
              onChange={handleChange}
            />
            <input
              type="text"
              name="last_name"
              placeholder="Soyad"
              onChange={handleChange}
            />
            <input
              type="email"
              name="email"
              placeholder="E-posta"
              onChange={handleChange}
            />
            <input
              type="text"
              name="phone_number"
              placeholder="Telefon Numarası"
              onChange={handleChange}
            />
          </>
        )}
        <input
          type="text"
          name="username"
          placeholder="Kullanıcı Adı"
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Şifre"
          onChange={handleChange}
        />
        <button type="submit">
          {formType === "login" ? "Giriş Yap" : "Kayıt Ol"}
        </button>
      </form>
      <p>{message}</p>
      <button onClick={() => setFormType(formType === "login" ? "register" : "login")}>
        {formType === "login" ? "Kayıt Ol" : "Giriş Yap"}
      </button>
    </div>
  );
};

export default AuthenticationPage;