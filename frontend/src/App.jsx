import React, { useEffect, useState } from 'react';
import axios from 'axios';
import UserForm from './components/UserForm';        // ✅ import par défaut

export default function App() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const { data } = await axios.get(
      `${process.env.REACT_APP_API_URL}/users`
    );
    setUsers(data);
  };

  // On charge la liste une seule fois au montage
  useEffect(() => {
    fetchUsers();
  }, []);

  const remove = async (id) => {
    await axios.delete(`${process.env.REACT_APP_API_URL}/users/${id}`, {
      headers: { 'X-Admin-Token': process.env.REACT_APP_ADMIN_PASSWORD },
    });
    fetchUsers();
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Utilisateurs</h1>
      {/* ✅ onSubmit (et non onAdded) */}
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
