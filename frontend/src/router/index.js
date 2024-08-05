import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/rectareamanage',
      name: 'rectareamanage',
      component: () => import('../views/rectAreaManageView.vue')
    },
    {
      path: '/tablerecgonize',
      name: 'tablerecgonize',
      component: () => import('../views/tablerecgonizeView.vue')
    },
    {
      path: '/tablercalibration',
      name: 'tablercalibration',
      component: () => import('../views/tablercalibrationView.vue')
    },
    {
      path: '/reportgeneration',
      name: 'reportgeneration',
      component: () => import('../views/reportgenerationView.vue')
    }
  ]
})

export default router
