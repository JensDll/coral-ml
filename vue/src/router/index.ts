import { h } from 'vue'
import {
  createRouter,
  createWebHistory,
  RouteRecordRaw,
  RouterView
} from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import MainPage from '../views/MainPage.vue'
import HomePage from '../views/HomePage.vue'

import RecordMain from '../views/record/RecordMain.vue'

import RecordUpload from '~/views/record/management/RecordUpload.vue'
import RecordOverview from '~/views/record/management/RecordOverview.vue'

import RecordImage from '~/views/record/ai/RecordImage.vue'
import RecordVideo from '~/views/record/ai/RecordVideo.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'landing-page',
    component: LandingPage
  },
  {
    path: '/ai',
    component: MainPage,
    children: [
      {
        path: '',
        name: 'home',
        component: HomePage
      },
      {
        path: 'record',
        component: { render: () => h(RouterView) },
        children: [
          {
            path: '',
            name: 'record',
            component: RecordMain
          },
          {
            path: 'upload/:recordTypeId',
            name: 'record-upload',
            component: RecordUpload
          },
          {
            path: 'overview/:recordTypeId',
            name: 'record-overview',
            component: RecordOverview
          }
        ]
      },
      {
        path: 'image-classification',
        name: 'image-classification',
        component: RecordImage
      },
      {
        path: 'object-detection',
        name: 'object-detection',
        component: RecordVideo
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
