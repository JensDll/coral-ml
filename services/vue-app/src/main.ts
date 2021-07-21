import { createApp } from 'vue'
import { router } from './router'
import { createPinia } from 'pinia'
import App from './App.vue'
import 'tailwindcss/tailwind.css'

declare global {
  interface Window {
    onLoadLinks: Record<number, 'image-classification' | 'video-analysis'>
    isRecordLoadedForCurrentRoute: boolean
  }
}

window.onLoadLinks = {
  2: 'image-classification',
  3: 'video-analysis'
}

const app = createApp(App).use(router).use(createPinia())
app.mount('#app')
