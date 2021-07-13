import { h } from 'vue'
import {
  createRouter,
  createWebHistory,
  RouteRecordRaw,
  RouterView
} from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import MainPage from '../views/ai/MainPage.vue'
import HomePage from '../views/ai/HomePage.vue'
import RecordMain from '../views/ai/record/RecordMain.vue'
import RecordUpload from '~/views/ai/record/RecordUpload.vue'
import RecordImage from '~/views/ai/record/RecordImage.vue'
import RecordOverview from '~/views/ai/record/RecordOverview.vue'
import RecordVideo from '~/views/ai/record/RecordVideo.vue'

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
        path: 'image',
        name: 'image',
        component: RecordImage
      },
      {
        path: 'video',
        name: 'video',
        component: RecordVideo
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
