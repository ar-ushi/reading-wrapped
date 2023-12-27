import { createApp } from 'vue';
import './style.scss';
import App from './App.vue';
import {vuetify} from './plugins/vuetify';
import router from './router';
import { createPinia } from 'pinia';
import '@mdi/font/css/materialdesignicons.css';

const app = createApp(App);
const pinia = createPinia();

app.use(vuetify).use(router).use(pinia).mount('#app');