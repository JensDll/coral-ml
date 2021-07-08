<template>
  <div class="grid-container">
    <v-header />
    <v-nav />
    <section class="main px-4 lg:pl-12">
      <router-view></router-view>
    </section>
  </div>
</template>

<script setup lang="ts">
import VHeader from "../components/layout/VHeader.vue"
import VNav from "../components/layout/VNav.vue"
</script>

<style scoped lang="postcss">
.grid-container {
  display: grid;
  row-gap: 4rem;
  height: 100%;
  grid-template-rows: auto 1fr;
  grid-template-columns: 16rem 1fr;
  grid-template-areas:
    "logo header"
    "main main";
}

.main {
  grid-area: main;
}

@screen lg {
  .grid-container {
    grid-template-areas:
      "logo header"
      "nav main";
  }
}
</style>
