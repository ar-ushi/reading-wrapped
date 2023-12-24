import { createVuetify } from 'vuetify'
import { components, directives } from 'vuetify/dist/vuetify-labs.js';


export const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#41b883',
          background: '#35495e',
          error: '#d63031',
          info: '#0984e3',
          secondary: '#fdcb6e',
          success: '#00cec9',
          surface: '#6c5ce7',
          warning: '#2d3436',
        },
        dark: false,
        variables: {},
      },
    },
  },
})