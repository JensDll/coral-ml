<template>
  <section class="cards">
    <slot></slot>
  </section>
</template>

<script setup lang="ts"></script>

<style lang="postcss" scoped>
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(20rem, 100%), 1fr));
}
</style>
