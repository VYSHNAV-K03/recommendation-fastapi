import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [userId, setUserId] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/users/${userId}`);
      localStorage.setItem("user", JSON.stringify(res.data));
      alert("Login successful!");
      navigate("/");
      window.location.reload();
    } catch {
      alert("User not found");
    }
  };

  return (
    <div className="container py-5">
      <div className="row align-items-center">
        {/* Illustration Image */}
        <div className="col-md-6 text-center">
          <img
            src="/images/login.svg"
            alt="Login Illustration"
            className="img-fluid"
            style={{ maxHeight: "400px" }}
          />
        </div>

        {/* Login Form */}
        <div className="col-md-6">
          <div className="card shadow p-4">
            <h2 className="text-center mb-4">Login</h2>
            <div className="mb-3">
              <label className="form-label">User ID</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter User ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
              />
            </div>
            <button className="btn btn-primary w-100" onClick={handleLogin}>
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
