<template>
  <main class="lg:container lg:mx-auto min-h-screen m:px-6">
    <router-view></router-view>
    <v-nav-toggle class="z-50 fixed bottom-4 right-4"></v-nav-toggle>
  </main>
</template>

<script setup lang="ts">
import VNavToggle from "./components/common/VNavToggle.vue"
</script>

<style lang="postcss">
@import url("https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");

#app {
  @apply font-body;
}
</style>
