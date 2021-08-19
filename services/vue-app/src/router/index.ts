import { h } from 'vue'
import {
  createRouter,
  createWebHistory,
  RouteRecordRaw,
  RouterView
} from 'vue-router'
import { recordRepository } from '~/api'

import LandingPage from '../views/LandingPage.vue'
import MainPage from '../views/MainPage.vue'
import HomePage from '../views/HomePage.vue'

import RecordUploadPage from '~/views/record/UploadPage.vue'
import RecordOverviewPage from '~/views/record/OverviewPage.vue'

import ImageClassificationPage from '~/views/classification/ImageClassificationPage.vue'
import VideoAnalysisPage from '~/views/video/VideoAnalysisPage.vue'

import RecordMain from '../views/record/MainPage.vue'

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
            component: RecordUploadPage
          },
          {
            path: 'overview/:recordTypeId',
            name: 'record-overview',
            component: RecordOverviewPage
          }
        ]
      },
      {
        path: 'image-classification',
        name: 'image-classification',
        component: ImageClassificationPage
      },
      {
        path: 'video-analysis',
        name: 'video-analysis',
        component: VideoAnalysisPage
      }
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
