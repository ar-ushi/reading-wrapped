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
          secondary: '#402be2',
          success: '#00cec9',
          surface: '#6c5ce7',
          warning: '#2d3436',
          text: '#000000',
        },
        dark: false
      },
        dark: {
          colors:{
            primary: '#5C148C',
            background: '#000000',
            secondary:'#9024d8',
            error: '#f73535',
            text: '#ffffff'
          }
        },
        variables: {},
      },
    },
  },
)