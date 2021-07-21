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

import RecordUpload from '~/views/explore-ai/record/UploadPage.vue'
import RecordOverview from '~/views/explore-ai/record/OverviewPage.vue'

import ImageClassification from '~/views/explore-ai/ImageClassification.vue'
import VideoAnalysis from '~/views/explore-ai/VideoAnalysis.vue'

import RecordMain from '../views/explore-ai/record/MainPage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'landing-page',
    component: LandingPage
  },
  {
    path: '/explore-ai',
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
        component: ImageClassification
      },
      {
        path: 'video-analysis',
        name: 'video-analysis',
        component: VideoAnalysis
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
