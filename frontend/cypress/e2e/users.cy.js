describe('Parcours création utilisateur', () => {
    it('crée un utilisateur et l’affiche dans la liste', () => {
      cy.visit('/');
  
      cy.get('input[name="email"]').type('test@cypress.com');
      cy.get('input[name="password"]').type('cypress123');
      cy.get('button[type="submit"]').click();
  
      // on vérifie que l'utilisateur apparaît
      cy.contains('test@cypress.com').should('be.visible');
    });
  });
  