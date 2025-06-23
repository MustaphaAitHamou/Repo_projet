// frontend/cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',

    // accepte *.cy.js OU *.spec.js partout sous cypress/
    specPattern: 'cypress/**/*.{cy,spec}.js',

    supportFile: false,
  },
});
