<template>
  <button
    class="
      focus:outline-none focus:ring focus:ring-offset-2
      transition-colors
      duration-200
    "
    :class="[
      { 'opacity-40 pointer-events-none': disabled },
      reverse ? `reverse-${type}` : type
    ]"
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
    type: String as PropType<"basic" | "primary" | "secondary" | "danger">,
    default: "primary"
  },
  reverse: {
    type: Boolean
  }
})
</script>

<style lang="postcss" scoped>
.basic,
.reverse-basic {
  @apply border-2 border-gray-300;

  &:hover {
    @apply bg-gray-50;
  }

  &:focus {
    @apply ring-gray-300;
  }
}

.primary {
  @apply bg-blue-500 text-white;

  &:hover {
    @apply bg-blue-400;
  }

  &:focus {
    @apply ring-blue-500;
  }
}

.secondary {
  @apply bg-emerald-500 text-white;

  &:hover {
    @apply bg-emerald-400;
  }

  &:focus {
    @apply ring-emerald-500;
  }
}

.danger {
  @apply bg-red-500 text-white;

  &:hover {
    @apply bg-red-400;
  }

  &:focus {
    @apply ring-red-500;
  }
}

.reverse-primary {
  @apply border-2 border-blue-500 text-blue-500;

  &:hover {
    @apply bg-blue-50;
  }

  &:focus {
    @apply ring-blue-500;
  }
}

.reverse-secondary {
  @apply border-2 border-emerald-500 text-emerald-500;

  &:hover {
    @apply bg-emerald-50;
  }

  &:focus {
    @apply ring-emerald-500;
  }
}

.reverse-danger {
  @apply border-2 border-red-500 text-red-500;

  &:hover {
    @apply bg-red-50;
  }

  &:focus {
    @apply ring-red-500;
  }
}
</style>
