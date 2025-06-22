import React, { useState } from 'react';
import axios from 'axios';

export function UserForm({ onAdded }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const submit = async e => {
    e.preventDefault();
    await axios.post(`${process.env.REACT_APP_API_URL}/users`, { email, password });
    setEmail(''); setPassword('');
    onAdded();
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: '1rem' }}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Ajouter</button>
    </form>
  );
}