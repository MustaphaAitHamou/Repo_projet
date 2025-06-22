describe('Flux utilisateur', () => {
    it('ajoute, liste et supprime un utilisateur', () => {
      cy.visit('/');
      cy.get('input[placeholder="Email"]').type('e2e@test.com');
      cy.get('input[placeholder="Password"]').type('1234');
      cy.contains('Ajouter').click();
      cy.contains('e2e@test.com').should('exist');
      cy.contains('Supprimer').click();
      cy.contains('e2e@test.com').should('not.exist');
    });
  });