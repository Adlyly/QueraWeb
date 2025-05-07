import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');

    if (!token) {
      navigate('/');
      return;
    }

    fetch('http://localhost:8000/admin-dashboard/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    })
    .then(res => {
      if (res.status === 403 || res.status === 401) {
        throw new Error("Unauthorized");
      }
      return res.json();
    })
    .then(data => {
      setMessage(data.message);
    })
    .catch(() => {
      alert("Access denied. Redirecting to login.");
      navigate('/');
    });
  }, []);

  const handleLogout = () => {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');

    fetch('http://localhost:8000/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });

    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>{message || "Loading..."}</h1>
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
};

export default AdminDashboard;
