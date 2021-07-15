<template>
  <div class="flex">
    <div
      v-for="(c, i) in ['outer', 'inner', 'outer']"
      :key="i"
      :class="[
        c,
        'w-5 h-5 rounded-full bg-blue-400 ml-2 first:ml-0',
        $attrs.class
      ]"
    ></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
  name: 'vloading',
  inheritAttrs: false
})
</script>

<style lang="postcss" scoped>
.outer {
  animation: a 600ms infinite;
}

.inner {
  animation: a 600ms 300ms infinite;
}

@keyframes a {
  50% {
    opacity: 0.7;
    transform: scale(0.8);
  }
}
</style>
