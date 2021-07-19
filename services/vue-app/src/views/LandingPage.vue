<template>
  <section class="pt-20 px-4">
    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold">
      Explore Artificial Intelligence
    </h1>
    <p class="text-lg sm:text-2xl my-8">
      Powered by SIMATIC Industrial PC and Coral Edge TPU
    </p>
    <div class="flex flex-col sm:flex-row">
      <v-button
        class="px-6 py-4 font-semibold rounded-xl"
        @click="router.push({ name: 'home' })"
      >
        Getting Started
      </v-button>
    </div>
  </section>
</template>

<script setup lang="ts">
import VButton from '~/components/base/VButton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style></style>
