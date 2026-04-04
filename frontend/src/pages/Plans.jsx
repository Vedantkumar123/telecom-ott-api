import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPlans } from '../api/planApi';
import { subscribeToPlan } from '../api/subscriptionApi';

const Plans = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [subscribing, setSubscribing] = useState(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const data = await getPlans();
        setPlans(data);
      } catch (err) {
        setError(err.response?.data?.detail || err.message || 'Failed to load plans');
      } finally {
        setLoading(false);
      }
    };
    fetchPlans();
  }, []);

  const handleSubscribe = async (planId) => {
    setSubscribing(planId);
    try {
      await subscribeToPlan(planId);
      alert('Subscribed successfully!');
      navigate('/subscriptions');
    } catch (err) {
      alert(err.response?.data?.detail || err.message || 'Subscription failed');
    } finally {
      setSubscribing(null);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading plans...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <header className="page-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>
        <h1 className="page-title">Available Plans</h1>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="plans-grid">
        {plans.map(plan => (
          <div key={plan._id || plan.id} className="plan-card">
            <div className="plan-header">
              <h3 className="plan-name">{plan.name}</h3>
              <div className="plan-price">
                <span className="currency">$</span>
                <span className="amount">{plan.price}</span>
                <span className="period">/month</span>
              </div>
            </div>
            <div className="plan-description">
              <p>Validity: {plan.validity_days} days</p>
            </div>
            <div className="plan-features">
              {plan.included_apps && plan.included_apps.map((feature, index) => (
                <div key={index} className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>{feature}</span>
                </div>
              ))}
            </div>
            <button
              onClick={() => handleSubscribe(plan._id || plan.id)}
              className="subscribe-button"
              disabled={subscribing === (plan._id || plan.id)}
            >
              {subscribing === (plan._id || plan.id) ? 'Subscribing...' : 'Subscribe Now'}
            </button>
          </div>
        ))}
      </div>

      {plans.length === 0 && !error && (
        <div className="empty-state">
          <h3>No plans available</h3>
          <p>Please check back later for available plans.</p>
        </div>
      )}
    </div>
  );
};

export default Plans;