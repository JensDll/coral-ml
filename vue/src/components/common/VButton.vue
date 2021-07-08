<template>
  <button
    class="
      focus:outline-none focus:ring focus:ring-offset-2
      transition-colors
      duration-200
    "
    :class="[{ 'opacity-40 pointer-events-none': disabled }, type]"
    :type="htmlType"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import type { PropType } from "vue"

const props = defineProps({
  loading: {
    type: Boolean
  },
  disabled: {
    type: Boolean
  },
  htmlType: {
    type: String as PropType<"button" | "submit" | "reset">,
    default: "button"
  },
  type: {
    type: String as PropType<"basic" | "primary" | "secondary">,
    default: "primary"
  }
})
</script>

<style lang="postcss" scoped>
.primary {
  @apply bg-blue-500 text-white;

  &:hover {
    @apply bg-blue-400;
  }

  &:focus {
    @apply ring-blue-400;
  }
}
.secondary {
  @apply bg-emerald-500 text-white;

  &:hover {
    @apply bg-emerald-400;
  }

  &:focus {
    @apply ring-emerald-400;
  }
}
</style>
