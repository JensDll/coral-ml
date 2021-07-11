import { createApp } from "vue"
import { router } from "./router"
import { storeKey, store } from "./composable/useStore"
import { socketServiceKey, socketService } from "./composable/useSocketService"
import App from "./App.vue"
import "tailwindcss/tailwind.css"

createApp(App)
  .provide(storeKey, store)
  .provide(socketServiceKey, socketService)
  .use(router)
  .mount("#app")
