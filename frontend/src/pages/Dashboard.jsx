import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { path: '/plans', label: 'Plans', icon: '📋' },
    { path: '/subscriptions', label: 'My Subscriptions', icon: '📺' },
    { path: '/content', label: 'Content Library', icon: '🎬' },
    { path: '/access-history', label: 'Access History', icon: '📊' },
    ...(user?.role === 'admin'
      ? [{ path: '/admin', label: 'Admin Dashboard', icon: '⚙️' }]
      : []),
  ];

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Telecom OTT Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.mobile_number || 'User'}</span>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
      </header>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h2>Welcome to your Telecom OTT Platform</h2>
          <p>Manage your subscriptions, browse content, and access your services.</p>
        </div>

        <div className="menu-grid">
          {menuItems.map((item) => (
            <div
              key={item.path}
              className="menu-card"
              onClick={() => navigate(item.path)}
            >
              <div className="menu-icon">{item.icon}</div>
              <h3>{item.label}</h3>
              <p>Access {item.label.toLowerCase()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;