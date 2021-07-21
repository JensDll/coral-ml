import { createApp } from 'vue'
import { router } from './router'
import { createPinia } from 'pinia'
import App from './App.vue'
import 'tailwindcss/tailwind.css'
import { RecordType } from './api'

declare global {
  interface Window {
    onLoadLinks: Record<RecordType, 'image-classification' | 'video-analysis'>
    isRecordLoadedForCurrentRoute: boolean
  }
}

window.onLoadLinks = {
  'Image Classification': 'image-classification',
  'Object Detection': 'video-analysis'
}

const app = createApp(App).use(router).use(createPinia())
app.mount('#app')
