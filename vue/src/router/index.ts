import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"
import LandingPage from "../views/LandingPage.vue"
import MainPage from "../views/MainPage.vue"
import HomePage from "../views/HomePage.vue"
import ImagePage from "../views/ImagePage.vue"
import VideoPage from "../views/VideoPage.vue"

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
        path: "video",
        name: "ai-video",
        component: VideoPage
      },
      {
        path: "image",
        name: "ai-image",
        component: ImagePage
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
