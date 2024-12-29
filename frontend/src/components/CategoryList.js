import React, { useState, useEffect } from 'react';
import { getAllCategories } from '../services/categoryApi';
import { useNavigate } from 'react-router-dom';
import '../styles/CategoryList.css';

const CategoryList = () => {
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      const categories = await getAllCategories();
      setCategories(categories);
    };

    fetchCategories();
  }, []);

  const handleCategoryClick = (categoryId) => {
    navigate(`/categories/${categoryId}`);
  };

  return (
    <div className="category-list">
      <h2 className="category-header">Categories</h2>
      <ul>
        {categories.map((category) => (
          <li key={category.category_id} onClick={() => handleCategoryClick(category.category_id)}>
            {category.category_name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CategoryList;
