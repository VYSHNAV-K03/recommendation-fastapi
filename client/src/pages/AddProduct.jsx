import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function AddProduct() {
  const [product, setProduct] = useState({
    item_id: "",
    name: "",
    category: "",
    price: "",
    brand: "",
    rating: "",
    image_url: "",
  });

  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  const handleChange = (e) => {
    setProduct({ ...product, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...product,
        item_id: parseInt(product.item_id),
        price: parseFloat(product.price),
        rating: parseFloat(product.rating),
        user_id: user.user_id,
      };
      await axios.post("http://localhost:8000/add_product", payload);
      alert("Product added successfully!");
      setProduct({
        item_id: "",
        name: "",
        category: "",
        price: "",
        brand: "",
        rating: "",
        image_url: "",
      });
    } catch (error) {
      alert("Failed to add product");
      console.error(error);
    }
  };

  return (
    <div className="container my-5">
      <div className="card shadow p-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3 className="mb-0">Add Product</h3>
          <button className="btn btn-secondary" onClick={() => navigate(-1)}>
            ← Back
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Item ID</label>
            <input
              type="number"
              name="item_id"
              className="form-control"
              value={product.item_id}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Name</label>
            <input
              name="name"
              className="form-control"
              value={product.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Category</label>
            <input
              name="category"
              className="form-control"
              value={product.category}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Price</label>
            <input
              type="number"
              name="price"
              step="0.01"
              className="form-control"
              value={product.price}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Brand</label>
            <input
              name="brand"
              className="form-control"
              value={product.brand}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Rating</label>
            <input
              type="number"
              step="0.1"
              name="rating"
              className="form-control"
              value={product.rating}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Image URL</label>
            <input
              name="image_url"
              className="form-control"
              value={product.image_url}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-success w-100">
            Add Product
          </button>
        </form>
      </div>
    </div>
  );
}

export default AddProduct;
