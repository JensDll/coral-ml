<template>
  <div :class="['rounded-md font-medium py-1 px-4', type]">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
  props: {
    type: {
      type: String,
      default: 'default'
    }
  }
})
</script>

<style lang="postcss" scoped>
.default {
  @apply bg-orange-50 text-orange-500;
}
</style>
