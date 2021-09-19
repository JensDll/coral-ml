import { createApp } from 'vue'
import { router } from './router'
import { createPinia } from 'pinia'
import { longPress } from './plugins'
import App from './App.vue'
import 'tailwindcss/tailwind.css'

window.onLoadLinks = {
  'Image Classification': 'image-classification',
  'Object Detection': 'video-analysis'
}

createApp(App).use(router).use(createPinia()).use(longPress).mount('#app')
