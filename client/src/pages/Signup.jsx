import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [form, setForm] = useState({
    user_id: "",
    name: "",
    age: "",
    location: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/add_user", form);
      alert("Signup successful!");
      navigate("/login");
    } catch (err) {
      alert("Signup failed: " + err.response?.data?.detail || "Unknown error");
    }
  };

  return (
    <div className="container py-5">
      <div className="row align-items-center">
        {/* Illustration Image */}
        <div className="col-md-6 text-center">
          <img
            src="/images/register.svg"
            alt="Signup illustration"
            className="img-fluid"
            style={{ maxHeight: "400px" }}
          />
        </div>

        {/* Signup Form */}
        <div className="col-md-6">
          <div className="card shadow p-4">
            <h2 className="text-center mb-4">Signup</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">User ID</label>
                <input
                  name="user_id"
                  className="form-control"
                  placeholder="Enter User ID"
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Name</label>
                <input
                  name="name"
                  className="form-control"
                  placeholder="Enter Name"
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Age</label>
                <input
                  name="age"
                  type="number"
                  className="form-control"
                  placeholder="Enter Age"
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="form-label">Location</label>
                <input
                  name="location"
                  className="form-control"
                  placeholder="Enter Location"
                  onChange={handleChange}
                  required
                />
              </div>
              <button type="submit" className="btn btn-success w-100">
                Signup
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Signup;
