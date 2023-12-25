import { createVuetify } from 'vuetify'
import { components, directives } from 'vuetify/dist/vuetify-labs.js';
import 'vuetify/dist/vuetify.min.css';


export const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme : 'light',
    themes: {
      light: {
        colors: {
          primary: '#6C5CE7',
          background: '#FFFFFF',
          error: '#d63031',
          info: '#0984e3',
          secondary: '#fdcb6e',
          success: '#00cec9',
          surface: '#6c5ce7',
          warning: '#2d3436',
        },
        dark: false
      },
        dark: {
          colors:{
            primary: '#5C148C',
            background: '#000000'
          }
        },
        variables: {},
      },
    },
  },
)