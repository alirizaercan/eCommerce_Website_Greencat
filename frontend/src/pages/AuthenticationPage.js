/* frontend/src/pages/AuthenticationPage.js */
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
      setMessage(response.message || "Error during login");
    } else {
      const response = await registerCustomer(formData);
      setMessage(response.message || "Error during registration");
    }
  };

  return (
    <div>
      <h1>{formType === "login" ? "Login" : "Register"}</h1>
      <form onSubmit={handleSubmit}>
        {formType === "register" && (
          <>
            <input
              type="text"
              name="first_name"
              placeholder="First Name"
              onChange={handleChange}
            />
            <input
              type="text"
              name="last_name"
              placeholder="Last Name"
              onChange={handleChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              onChange={handleChange}
            />
            <input
              type="text"
              name="phone_number"
              placeholder="Phone Number"
              onChange={handleChange}
            />
          </>
        )}
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
        />
        <button type="submit">
          {formType === "login" ? "Login" : "Register"}
        </button>
      </form>
      <p>{message}</p>
      <button onClick={() => setFormType(formType === "login" ? "register" : "login")}>
        Switch to {formType === "login" ? "Register" : "Login"}
      </button>
    </div>
  );
};

export default AuthenticationPage;
