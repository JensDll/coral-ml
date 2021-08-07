<template>
  <div
    class="
      flex
      items-center
      cursor-pointer
      hover:text-indigo-700
      pl-6
      py-6
      sticky
      border-b
      bg-white
      z-10
      top-0
      lg:pl-4
    "
    @click="goHome()"
  >
    <AcademicCapIcon class="w-6 h-6" />
    <span class="uppercase tracking-wider font-semibold ml-4">Explore AI</span>
  </div>
  <header
    class="
      header
      flex
      justify-between
      border-b
      py-6
      pr-6
      sticky
      top-0
      bg-white
      z-10
      lg:pr-0 lg:ml-12
    "
  >
    <div>
      <v-link href="https://coral.ai/models/">Coral AI</v-link>
    </div>
    <div>
      <v-link href="https://github.com/JensDll/coral-ml">GitHub</v-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { AcademicCapIcon } from '@heroicons/vue/solid'
import VLink from '../base/BaseLink.vue'
const router = useRouter()

function goHome() {
  router.push({ name: 'landing-page' })
}
</script>

<style lang="postcss" scoped>
.header {
  grid-area: header;
}
</style>
