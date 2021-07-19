<template>
  <main class="main px-6 pb-24 lg:pr-0 lg:pl-12">
    <router-view></router-view>
  </main>
</template>

<script setup lang="ts"></script>

<style scoped lang="postcss">
.main {
  grid-area: main;
}
</style>
