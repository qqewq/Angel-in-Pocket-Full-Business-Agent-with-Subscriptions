import React, { useState } from 'react';

export default function IdeaForm() {
  const [idea, setIdea] = useState('');
  const token = localStorage.getItem('token') || '';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/ideas/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ idea })
    });
    const data = await res.json();
    if (res.ok) {
      alert(`Project created: ${data.project_id}`);
    } else {
      alert(`Error: ${data.detail || JSON.stringify(data)}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Submit Your Business Idea</h2>
      <textarea value={idea} onChange={(e) => setIdea(e.target.value)} placeholder="Describe your idea..." required />
      <button type="submit">Submit Idea</button>
    </form>
  );
}
