import React, { useState } from 'react';

export default function UserForm({ onSubmit }) {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email:
        <input
          type="email"
          name="email"
          aria-label="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
      </label>
      <label>
        Mot de passe:
        <input
          type="password"
          name="password"
          aria-label="Mot de passe"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
      </label>
      <button type="submit">Envoyer</button>
    </form>
  );
}
