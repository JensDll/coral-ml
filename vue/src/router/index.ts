import { h } from "vue"
import {
  createRouter,
  createWebHistory,
  RouteRecordRaw,
  RouterView
} from "vue-router"
import LandingPage from "../views/LandingPage.vue"
import MainPage from "../views/ai/MainPage.vue"
import HomePage from "../views/ai/HomePage.vue"
import ModelPage from "../views/ai/model/ModelPage.vue"
import ModelUploadNew from "~/views/ai/model/ModelUploadNew.vue"
import ModelImagePage from "~/views/ai/model/ModelImagePage.vue"

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "landing-page",
    component: LandingPage
  },
  {
    path: "/ai",
    component: MainPage,
    children: [
      {
        path: "",
        name: "home",
        component: HomePage
      },
      {
        path: "model",
        component: { render: () => h(RouterView) },
        children: [
          {
            path: "",
            name: "model",
            component: ModelPage
          },
          {
            path: "upload",
            name: "model-new",
            component: ModelUploadNew
          }
        ]
      },
      {
        path: "image",
        name: "image",
        component: ModelImagePage
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
