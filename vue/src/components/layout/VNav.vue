<template>
  <nav
    v-if="!store.state.navHidden"
    v-bind="$attrs"
    class="
      nav
      bg-white
      fixed
      top-0
      bottom-0
      left-0
      z-50
      w-4/5
      p-4
      lg:static lg:p-0 lg:z-0 lg:w-full
    "
  >
    <ul class="lg:sticky lg:top-28">
      <li>
        <router-link class="link" :to="{ name: 'home' }">Home</router-link>
      </li>
      <li class="mt-6">
        <h5 class="px-3 mb-3 uppercase tracking-wider font-semibold">
          Getting Started
        </h5>
        <router-link class="link" :to="{ name: 'ai-image' }">
          Classification
        </router-link>
      </li>
      <li>
        <router-link class="link" :to="{ name: 'ai-video' }">
          Video Analysis
        </router-link>
      </li>
    </ul>
  </nav>
  <div
    v-if="!store.state.navHidden"
    class="fixed bg-black inset-0 z-40 bg-opacity-25 lg:hidden"
    @click="store.actions.toggleNav()"
  ></div>
</template>

<script setup lang="ts">
import { useStore } from "../../composable"

const store = useStore()
</script>

<style lang="postcss" scoped>
.nav {
  grid-area: nav;
}

.link {
  @apply px-3 py-2 rounded-lg block text-gray-500 transition-colors duration-200;

  &:hover {
    @apply text-gray-900;
  }
}

.router-link-exact-active {
  @apply bg-cyan-50 text-cyan-700 font-medium;
}
</style>
