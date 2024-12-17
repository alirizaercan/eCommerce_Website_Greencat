import React from "react";
import Header from "../components/Header";

const MainPage = () => {
  const isLoggedIn = true; // Backend'den gelecek gerçek değer
  const customerFirstName = "Ali"; // Örnek kullanıcı adı, backend'den çekilecek

  const handleSearch = (searchTerm) => {
    console.log(`Searching for: ${searchTerm}`);
    // Backend'den ürünleri filtrelemek için API çağrısı burada yapılabilir.
  };

  return (
    <div className="main-page">
      <h1 className="main-header">Welcome to Our E-Commerce Platform</h1>
      {/* Header Bileşeni */}
      <Header
        isLoggedIn={isLoggedIn}
        customerFirstName={customerFirstName}
        onSearch={handleSearch}
      />
    </div>
  );
};

export default MainPage;
