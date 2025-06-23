import React, { useState, useEffect } from "react";
import axios from "axios";

const baseURL = "http://localhost:8000";

function RecommendationForm() {
  const [itemId, setItemId] = useState("101");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [type, setType] = useState("");
  const [allUsers, setAllUsers] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")));

  const userId = user ? user.user_id : "";

  console.log(user);
  console.log(recommendations);

  // ✅ Fetch hybrid (collaborative + age-based) on mount
  useEffect(() => {
    if (userId) {
      fetchHybridRecommendations();
    }
  }, [userId]);

  const fetchHybridRecommendations = async () => {
    setLoading(true);
    setType("hybrid");
    try {
      const response = await axios.post(`${baseURL}/recommend/hybrid`, {
        user_id: parseInt(userId),
        item_id: parseInt(itemId),
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      console.error(err);
      alert("Error fetching hybrid recommendations.");
    }
    setLoading(false);
  };

  const fetchAllUsers = async () => {
    try {
      const response = await axios.get(`${baseURL}/users`);
      setAllUsers(response.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching users.");
    }
  };

  const fetchAllItems = async () => {
    try {
      const response = await axios.get(`${baseURL}/items`);
      setAllItems(response.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching items.");
    }
  };

  const handleContentBased = async (selectedItemId) => {
    setLoading(true);
    setType("content-based");
    try {
      const response = await axios.post(`${baseURL}/recommend/content-based`, {
        user_id: parseInt(userId),
        item_id: parseInt(selectedItemId),
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      console.error(err);
      alert("Error fetching content-based recommendations.");
    }
    setLoading(false);
  };

  return (
    <div className="container mt-5 animate__animated animate__fadeIn">
      <div className="card shadow p-4">
        <h2 className="text-center mb-4 text-primary">Get Recommendations</h2>

        {/* <div className="row mb-3">
          <div className="col-md-6 mb-2">
            <input
              type="number"
              className="form-control"
              placeholder="Item ID"
              value={itemId}
              onChange={(e) => setItemId(e.target.value)}
            />
          </div>
        </div>

        <div className="d-flex justify-content-center mb-4">
          <button
            className="btn btn-outline-primary"
            onClick={handleContentBased}
          >
            Get Content-Based Recommendations
          </button>
        </div> */}

        {loading && (
          <div className="text-center mb-3">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="mt-2">Loading {type} recommendations...</p>
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="animate__animated animate__fadeInUp">
            <h4 className="text-center mb-3">Recommended Items</h4>
            <div className="row">
              {recommendations.map((item) => (
                <div
                  key={item.item_id}
                  className="col-md-3 mb-4"
                  onClick={() => handleContentBased(item.item_id)}
                  style={{ cursor: "pointer" }}
                >
                  <div className="card h-100 shadow-sm">
                    <img
                      src={item.image_url}
                      className="card-img-top"
                      alt={item.name}
                      style={{ height: "150px", objectFit: "cover" }}
                    />
                    <div className="card-body text-center">
                      <h5 className="card-title">{item.name}</h5>
                      <p className="card-text">
                        <strong>ID:</strong> {item.item_id}
                      </p>
                      <p className="card-text">
                        <strong>Price:</strong> ₹{item.price}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="d-flex flex-wrap justify-content-center gap-2 m-4">
        <button className="btn btn-info" onClick={fetchAllUsers}>
          Show All Users
        </button>
        <button className="btn btn-secondary" onClick={fetchAllItems}>
          Show All Items
        </button>
        <a href="/add_product" className="btn btn-secondary">
          Add Product
        </a>
      </div>

      {allUsers.length > 0 && (
        <div className="mt-5">
          <h4 className="text-center mb-3">All Users</h4>
          <ul className="list-group">
            {allUsers.map((user) => (
              <li key={user.user_id} className="list-group-item">
                ID: {user.user_id}, Name: {user.name}
              </li>
            ))}
          </ul>
        </div>
      )}

      {allItems.length > 0 && (
        <div className="mt-5">
          <h4 className="text-center mb-3">All Items</h4>
          <div className="row">
            {allItems.map((item) => (
              <div key={item.item_id} className="col-md-4 mb-4">
                <div className="card h-100 shadow-sm">
                  <img
                    src={item.image_url}
                    className="card-img-top"
                    alt={item.name}
                    style={{ height: "200px", objectFit: "cover" }}
                  />
                  <div className="card-body">
                    <h5 className="card-title text-center">{item.name}</h5>
                    <p className="card-text">
                      <strong>ID:</strong> {item.item_id}
                    </p>
                    <p className="card-text">
                      <strong>Price:</strong> ₹{item.price}
                    </p>
                    <p className="card-text">
                      <strong>Category:</strong> {item.category}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default RecommendationForm;
