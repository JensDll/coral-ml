import { createApp } from "vue"
import { router } from "./router"
import { storeKey, createStore } from "./composable/useStore"
import App from "./App.vue"
import "tailwindcss/tailwind.css"

createApp(App).provide(storeKey, createStore()).use(router).mount("#app")
