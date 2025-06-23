import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

/* -------------------------------------------------------------------------- */
/* 1.  MOCK AXIOS : aucune requête réseau réelle                               */
/* -------------------------------------------------------------------------- */
jest.mock('axios', () => ({
  get:    jest.fn().mockResolvedValue({ data: [] }),
  delete: jest.fn().mockResolvedValue({}),
}));

/* -------------------------------------------------------------------------- */
/* 2.  TEST                                                                    */
/*    - on rend le composant dans un act(async...)                             */
/*    - on attend une micro-tâche pour laisser le useEffect se terminer        */
/* -------------------------------------------------------------------------- */
test('affiche le titre', async () => {
  await act(async () => {
    render(<App />);
    await Promise.resolve();        // ← flush micro-tasks (résolution du mock Axios)
  });

  const heading = screen.getByRole('heading', { level: 1 });
  expect(heading).toHaveTextContent('Utilisateurs');
});
    