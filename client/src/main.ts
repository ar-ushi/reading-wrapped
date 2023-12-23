import { createApp } from 'vue'
import './style.scss'
import App from './App.vue'
import {createVuetify} from 'vuetify'
import { components, directives } from 'vuetify/dist/vuetify-labs.js';

const app = createApp(App);
const vuetify = createVuetify({
    components,
    directives,
})
app.use(vuetify).mount('#app');