import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/ProductTracker.vue')
      },
      {
        path: '/rank-check',
        component: () => import('pages/RankChecker.vue')
      }
    ],
  },
];

export default routes;
