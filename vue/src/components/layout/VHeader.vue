<template>
  <div
    class="
      flex
      items-center
      cursor-pointer
      hover:text-indigo-700
      pl-4
      py-6
      sticky
      border-b
      bg-white
      z-10
      top-0
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
      pr-4
      sticky
      top-0
      bg-white
      z-10
      lg:ml-12
    "
  >
    <div>
      <a
        href="https://coral.ai/models/"
        class="text-indigo-500 hover:text-indigo-700 ml-4"
      >
        Coral AI
      </a>
      <a
        href="https://tfhub.dev/"
        class="text-indigo-500 hover:text-indigo-700 ml-4"
      >
        TensorFlow Hub
      </a>
    </div>
    <div>
      <a
        href="https://github.com/JensDll/coral-ml"
        class="text-indigo-500 hover:text-indigo-700"
      >
        GitHub
      </a>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import { AcademicCapIcon } from "@heroicons/vue/solid"

const router = useRouter()

function goHome() {
  router.push({ name: "landing-page" })
}
</script>

<style lang="postcss" scoped>
.header {
  grid-area: header;
}
</style>
