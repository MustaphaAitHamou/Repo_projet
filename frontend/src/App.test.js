import { render, screen } from '@testing-library/react';
import App from './App';

test('affiche le titre', () => {
  render(<App />);
  // Suppose que dans App.js tu as <h1>Ma super app</h1>
  expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Ma super app');
});
