import { createApp } from 'vue'
import { router } from './router'
import { storeKey, store } from './composable/useStore'
import App from './App.vue'
import 'tailwindcss/tailwind.css'

createApp(App).provide(storeKey, store).use(router).mount('#app')
