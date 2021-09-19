import { RouteRecordRaw } from 'vue-router'
import Main from '~/views/image-classification/Main.vue'

export const imageClassificationRoutes: RouteRecordRaw[] = [
  {
    path: 'image-classification',
    name: 'image-classification',
    component: Main
  }
]
