<template>
  <transition name="slide">
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
        w-8/12
        p-6
        lg:relative lg:p-0 lg:z-0 lg:w-full
      "
    >
      <ul class="lg:fixed">
        <li>
          <router-link class="link" :to="{ name: 'home' }">Home</router-link>
        </li>
        <li class="mt-6">
          <h5 class="px-4 mb-3 uppercase tracking-wider font-semibold">
            Getting Started
          </h5>
          <router-link
            class="link"
            :to="{ name: 'record' }"
            active-class="getting-started-active"
          >
            Manage Models
          </router-link>
          <router-link class="link" :to="{ name: 'image-classification' }">
            Classification
          </router-link>
          <router-link class="link" :to="{ name: 'object-detection' }">
            Object Detection
          </router-link>
        </li>
      </ul>
    </nav>
  </transition>
  <transition name="fade">
    <div
      v-if="!store.state.navHidden"
      class="fixed bg-black inset-0 z-40 bg-opacity-25 lg:hidden"
      @click="store.actions.toggleNav()"
    ></div>
  </transition>
</template>

<script setup lang="ts">
import { useStore } from '../../composable'

const store = useStore()
</script>

<style lang="postcss" scoped>
.nav {
  grid-area: nav;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.link {
  @apply px-4 py-2 rounded-lg block text-gray-500 transition-colors duration-200;

  &:hover {
    @apply text-gray-900;
  }
}

.router-link-exact-active,
.getting-started-active {
  @apply bg-cyan-50 text-cyan-700 font-medium;
}
</style>
