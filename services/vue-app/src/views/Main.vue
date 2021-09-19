<template>
  <div class="grid-container lg:px-6">
    <TheHeader />
    <TheNav />
    <TheMain />
  </div>
</template>

<script setup lang="ts">
import TheHeader from '~/components/layout/TheHeader.vue'
import TheNav from '~/components/layout/TheNav.vue'
import TheMain from '~/components/layout/TheMain.vue'
</script>

<style scoped lang="postcss">
.grid-container {
  display: grid;
  row-gap: 2rem;
  height: 100%;
  grid-template-rows: auto 1fr;
  grid-template-columns: auto 1fr;
  grid-template-areas:
    'logo header'
    'main main';
}

@screen lg {
  .grid-container {
    row-gap: 3rem;
    grid-template-columns: 16rem 1fr;
    grid-template-areas:
      'logo header'
      'nav main';
  }
}

@screen xl {
  .grid-container {
    row-gap: 4rem;
  }
}
</style>
