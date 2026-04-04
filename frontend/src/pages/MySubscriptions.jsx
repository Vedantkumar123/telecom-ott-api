import React, { useState, useEffect } from 'react';
import { getMySubscriptions } from '../api/subscriptionApi';

const MySubscriptions = () => {
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const data = await getMySubscriptions();
        setSubscriptions(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchSubscriptions();
  }, []);

  return (
    <div>
      <h2>My Subscriptions</h2>
      <ul>
        {subscriptions.map(sub => (
          <li key={sub._id}>
            Plan ID: {sub.plan_id} - Status: {sub.status}
            {sub.start_date && ` - Start: ${new Date(sub.start_date).toLocaleString()}`}
            {sub.end_date && ` - End: ${new Date(sub.end_date).toLocaleString()}`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MySubscriptions;