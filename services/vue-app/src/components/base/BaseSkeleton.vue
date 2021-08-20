<template>
  <div class="v-skeleton-card" ref="cardRef">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, Ref } from 'vue'

const cardRef = ref() as Ref<HTMLElement>

const observer = new ResizeObserver(([card]) => {
  const target = card.target as HTMLElement
  target.style.setProperty('--card-width', `${card.contentRect.width}px`)
})

onMounted(() => {
  observer.observe(cardRef.value)
})

onBeforeUnmount(() => {
  observer.unobserve(cardRef.value)
})
</script>

<style lang="postcss" scoped>
.v-skeleton-card:deep(div.skeleton-item) {
  position: relative;
  overflow: hidden;
}

.v-skeleton-card:deep(div.skeleton-item::after) {
  content: '';
  position: absolute;
  width: calc(4 * var(--card-width));
  height: 100%;
  top: 0;
  left: 0;
  background: linear-gradient(
    90deg,
    theme('colors.gray.200') 18%,
    theme('colors.gray.100') 23%,
    theme('colors.gray.100') 27%,
    theme('colors.gray.200') 32%,
    theme('colors.gray.200') 68%,
    theme('colors.gray.100') 73%,
    theme('colors.gray.100') 77%,
    theme('colors.gray.200') 82%
  );
  transform: translateX(-75%);
  animation: load 0.7s linear infinite;
}

@keyframes load {
  100% {
    transform: translateX(-25%);
  }
}
</style>
