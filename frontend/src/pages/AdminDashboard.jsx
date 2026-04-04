import React, { useState } from 'react';
import { addContent } from '../api/contentApi';
import { createPlan } from '../api/planApi';

const AdminDashboard = () => {
  const [contentData, setContentData] = useState({ title: '', platform: '', category: '' });
  const [planData, setPlanData] = useState({ name: '', price: 0, validity_days: 30, included_apps: '' });
  const [error, setError] = useState('');

  const handleContentChange = (e) => {
    setContentData({ ...contentData, [e.target.name]: e.target.value });
  };

  const handlePlanChange = (e) => {
    const { name, value } = e.target;
    if (name === 'price' || name === 'validity_days') {
      setPlanData({ ...planData, [name]: Number(value) });
      return;
    }
    setPlanData({ ...planData, [name]: value });
  };

  const handleAddContent = async (e) => {
    e.preventDefault();
    try {
      await addContent(contentData);
      alert('Content added');
      setContentData({ title: '', platform: '', category: '' });
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreatePlan = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        name: planData.name,
        price: Number(planData.price),
        validity_days: Number(planData.validity_days),
        included_apps: planData.included_apps
          .split(',')
          .map((app) => app.trim())
          .filter(Boolean),
      };

      await createPlan(payload);
      alert('Plan created');
      setPlanData({ name: '', price: 0, validity_days: 30, included_apps: '' });
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {error && <p>{error}</p>}
      
      <h3>Add Content</h3>
      <form onSubmit={handleAddContent}>
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={contentData.title}
          onChange={handleContentChange}
          required
        />
        <input
          type="text"
          name="platform"
          placeholder="Platform (e.g. Netflix)"
          value={contentData.platform}
          onChange={handleContentChange}
          required
        />
        <input
          type="text"
          name="category"
          placeholder="Category (e.g. Movies)"
          value={contentData.category}
          onChange={handleContentChange}
          required
        />
        <button type="submit">Add Content</button>
      </form>

      <h3>Create Plan</h3>
      <form onSubmit={handleCreatePlan}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={planData.name}
          onChange={handlePlanChange}
          required
        />
        <input
          type="number"
          name="price"
          placeholder="Price"
          value={planData.price}
          onChange={handlePlanChange}
          required
        />
        <input
          type="number"
          name="validity_days"
          placeholder="Validity Days"
          value={planData.validity_days}
          onChange={handlePlanChange}
          required
        />
        <input
          type="text"
          name="included_apps"
          placeholder="Included Apps (comma separated)"
          value={planData.included_apps}
          onChange={handlePlanChange}
          required
        />
        <button type="submit">Create Plan</button>
      </form>

      <a href="/dashboard">Back to Dashboard</a>
    </div>
  );
};

export default AdminDashboard;