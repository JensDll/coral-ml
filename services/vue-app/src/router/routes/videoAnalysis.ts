import { RouteRecordRaw } from 'vue-router'
import Main from '~/views/video-analysis/Main.vue'

export const videoAnalysisRoutes: RouteRecordRaw[] = [
  {
    path: 'video-analysis',
    name: 'video-analysis',
    component: Main
  }
]
