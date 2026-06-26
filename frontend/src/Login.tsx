import React, { useState } from 'react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    const res = await fetch('/auth/login', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
      alert('Logged in');
    } else {
      alert('Login failed');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  );
}
