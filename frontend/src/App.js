import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthenticationPage from './pages/AuthenticationPage';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage'; // LoginPage ekledim, çünkü dizinde yer alıyor.
import RegisterPage from './pages/RegisterPage'; // RegisterPage ekledim, çünkü dizinde yer alıyor.

function App() {
  return (
    <Router>
      <Routes>
        {/* Ana rotalar */}
        <Route path="/" element={<AuthenticationPage />} />
        <Route path="/dashboard" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* LoginPage rotası */}
        <Route path="/register" element={<RegisterPage />} /> {/* RegisterPage rotası */}
      </Routes>
    </Router>
  );
}

export default App;
