import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { login, register } from '../api/authApi';

const Login = () => {
  const { login: authLogin } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ mobile_number: '', password: '', role: 'customer' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let data;
      if (isLogin) {
        data = await login({
          mobile_number: credentials.mobile_number,
          password: credentials.password,
        });
      } else {
        await register(credentials);
        // After register, login
        data = await login({
          mobile_number: credentials.mobile_number,
          password: credentials.password,
        });
      }

      authLogin({ mobile_number: credentials.mobile_number }, data.access_token);
      window.location.href = '/dashboard';
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">{isLogin ? 'Login' : 'Register'}</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="mobile_number">Mobile Number</label>
            <input
              type="text"
              id="mobile_number"
              name="mobile_number"
              placeholder="Enter your mobile number"
              value={credentials.mobile_number}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Enter your password"
              value={credentials.password}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="role">Role</label>
              <select
                id="role"
                name="role"
                value={credentials.role}
                onChange={handleChange}
                className="form-input"
              >
                <option value="customer">Customer</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          )}
          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register')}
          </button>
        </form>
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="auth-toggle"
          disabled={loading}
        >
          {isLogin ? 'Need to register?' : 'Already have an account?'}
        </button>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default Login;