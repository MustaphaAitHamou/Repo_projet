import React, { useState } from 'react';

/**
 * Formulaire de création d’utilisateur.
 * Appelle onSubmit({ email, password }) puis réinitialise les champs.
 */
export default function UserForm({ onSubmit }) {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ email, password });
    setEmail('');
    setPassword('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email&nbsp;:
        <input
          type="email"
          name="email"
          aria-label="Email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </label>

      <label>
        Mot de passe&nbsp;:
        <input
          type="password"
          name="password"
          aria-label="Password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>

      <button type="submit">Ajouter</button>
    </form>
  );
}
