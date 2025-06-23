import { render, screen, fireEvent } from '@testing-library/react';
import UserForm from './UserForm';

test('affiche les champs et déclenche onSubmit avec les bonnes valeurs', () => {
  const handleSubmit = jest.fn();
  render(<UserForm onSubmit={handleSubmit} />);

  // Remplit les champs
  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: 'a@b.c' },
  });
  fireEvent.change(screen.getByLabelText(/mot de passe/i), {
    target: { value: 'secret' },
  });

  // Clique sur le bouton "Ajouter"
  fireEvent.click(screen.getByRole('button', { name: /ajouter/i }));

  // Vérifie les valeurs transmises
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'a@b.c',
    password: 'secret',
  });
});
