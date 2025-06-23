import React, { useEffect, useState } from 'react';
import axios from 'axios';
import UserForm from './components/UserForm';

const API = process.env.REACT_APP_API_URL;

export default function App() {
  const [users, setUsers] = useState([]);

  /* ─── Lecture de la liste ─── */
  const fetchUsers = async () => {
    const { data } = await axios.get(`${API}/users`);
    setUsers(data);
  };

  /* ─── Création d’utilisateur ─── */
  const addUser = async ({ email, password }) => {
    await axios.post(`${API}/users`, { email, password });
    fetchUsers();
  };

  /* ─── Suppression ─── */
  const remove = async (id) => {
    await axios.delete(`${API}/users/${id}`, {
      headers: {
        'X-Admin-Token': process.env.REACT_APP_ADMIN_PASSWORD,
      },
    });
    fetchUsers();
  };

  /* Charge la liste au montage */
  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Utilisateurs</h1>

      {/* Formulaire d’ajout */}
      <UserForm onSubmit={addUser} />

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
