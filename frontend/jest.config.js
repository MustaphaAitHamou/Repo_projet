module.exports = {
    /* ---------------------------------------------------------------------- */
    /*  ENVIRONNEMENT & TRANSFORM                                             */
    /* ---------------------------------------------------------------------- */
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'jsx'],
    transform: { '^.+\\.(js|jsx)$': 'babel-jest' },
  
    /* ---------------------------------------------------------------------- */
    /*  MAPPINGS POUR LES IMPORTS CSS                                         */
    /* ---------------------------------------------------------------------- */
    moduleNameMapper: {
      '\\.(css|scss)$': 'identity-obj-proxy',
    },
  
    /* ---------------------------------------------------------------------- */
    /*  IGNORER LES FICHIERS CYPRESS POUR JEST                                */
    /*     – dossiers  /cypress/  et  src/cypress/                            */
    /*     – tout fichier qui termine par .cy.js                              */
    /* ---------------------------------------------------------------------- */
    testPathIgnorePatterns: [
      '/node_modules/',
      '/cypress/',
      '/src/cypress/',
    ],
    testRegex: '(/__tests__/.*|(\\.|/)(test))\\.jsx?$',   // Jest ne prend plus *.spec.js
  
    /* ---------------------------------------------------------------------- */
    /*  EXTENSIONS JEST-DOM                                                  */
    /* ---------------------------------------------------------------------- */
    setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  };
  