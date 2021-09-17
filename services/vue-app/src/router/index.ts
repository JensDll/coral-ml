import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { recordRepository } from '~/api'
import {
  imageClassificationRoutes,
  videoAnalysisRoutes,
  recordManagementRoutes
} from './routes'

import Landing from '../views/Landing.vue'
import Main from '../views/Main.vue'
import Home from '../views/Home.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'landing',
    component: Landing
  },
  {
    path: '/explore-ai',
    component: Main,
    children: [
      {
        path: '',
        name: 'home',
        component: Home
      },
      ...recordManagementRoutes,
      ...imageClassificationRoutes,
      ...videoAnalysisRoutes
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from) => {
  recordRepository.loadLoaded().then()
})
