// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../views/LandingPage.vue';
import YearWrapped from '../views/YearWrapped.vue';
import CurrentReadingStatus from '../views/CurrentReadingStatus.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage,
  },
  {
    path: '/wrapped/:uid',
    name: 'Wrapped',
    component: YearWrapped,
    props: true
  },
  {
    path: '/reading-status/:uid',
    component: CurrentReadingStatus,
    name: 'Reading Status',
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
