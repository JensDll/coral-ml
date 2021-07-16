<template>
  <section class="cards">
    <slot></slot>
  </section>
</template>

<script setup lang="ts"></script>

<style lang="postcss" scoped>
.cards {
  display: grid;
  column-gap: 4rem;
  row-gap: 3rem;
  place-items: start;
  grid-template-columns: repeat(auto-fit, minmax(min(20rem, 100%), 1fr));
}
</style>
