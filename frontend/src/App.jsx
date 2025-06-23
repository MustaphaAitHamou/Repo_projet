// frontend/src/App.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import UserForm from './components/UserForm';

export default function App() {
  const [users, setUsers] = useState([]);

  /* ------------------------------------------------------------------ */
  /* 1) Récupération de la liste des utilisateurs                       */
  /* ------------------------------------------------------------------ */
  const fetchUsers = async () => {
    const { data } = await axios.get(
      `${process.env.REACT_APP_API_URL}/users`
    );
    setUsers(data);
  };

  /* Charge la liste au montage du composant */
  useEffect(() => {
    fetchUsers();
  }, []);

  /* ------------------------------------------------------------------ */
  /* 2) Suppression d'un utilisateur                                    */
  /* ------------------------------------------------------------------ */
  const remove = async (id) => {
    await axios.delete(
      `${process.env.REACT_APP_API_URL}/users/${id}`,
      {
        headers: {
          // .env ➜ REACT_APP_ADMIN_PASSWORD
          'X-Admin-Token': process.env.REACT_APP_ADMIN_PASSWORD,
        },
      }
    );
    fetchUsers(); // rafraîchit la liste
  };

  /* ------------------------------------------------------------------ */
  /* 3) Rendu                                                           */
  /* ------------------------------------------------------------------ */
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Utilisateurs</h1>

      {/* UserForm déclenchera fetchUsers après création */}
      <UserForm onSubmit={fetchUsers} />

      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.email} {u.is_admin && '(admin)'}{' '}
            <button onClick={() => remove(u.id)}>Supprimer</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
