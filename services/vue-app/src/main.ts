import { createApp } from 'vue'
import { router } from './router'
import { createPinia } from 'pinia'
import { RecordType } from './api'
import { longPress } from './plugins'
import App from './App.vue'
import 'tailwindcss/tailwind.css'

declare global {
  interface Window {
    onLoadLinks: Record<RecordType, 'image-classification' | 'video-analysis'>
  }
}

window.onLoadLinks = {
  'Image Classification': 'image-classification',
  'Object Detection': 'video-analysis'
}

const app = createApp(App).use(router).use(createPinia()).use(longPress)

app.mount('#app')
