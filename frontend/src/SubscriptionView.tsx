import React, { useState } from 'react';

export default function SubscriptionView() {
  const [plan, setPlan] = useState('pro');
  const token = localStorage.getItem('token') || '';

  const handleSubscribe = async () => {
    const res = await fetch('/subscriptions/create-checkout-session?plan=' + plan, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (res.status === 401) {
      alert('Please login first');
      return;
    }
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      alert('Error: ' + JSON.stringify(data));
    }
  };

  const handleCancel = async () => {
    const res = await fetch('/subscriptions/cancel', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) alert('Subscription canceled');
  };

  return (
    <div>
      <h2>Choose Your Plan</h2>
      <select value={plan} onChange={(e) => setPlan(e.target.value)}>
        <option value="pro">Pro ($29/month)</option>
        <option value="enterprise">Enterprise ($99/month)</option>
      </select>
      <button onClick={handleSubscribe}>Subscribe</button>
      <br />
      <button onClick={handleCancel}>Cancel Subscription</button>
    </div>
  );
}
