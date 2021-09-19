<template>
  <div
    :class="['rounded-md font-medium py-1 px-4 flex items-center', badgeType]"
  >
    <slot></slot>
    <LoadingIcon class="ml-4 w-4 h-4" v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import { PropType, computed } from 'vue'
import LoadingIcon from '../icons/LoadingIcon.vue'

type BadgeType = 'loading' | 'default'

const props = defineProps({
  type: {
    type: String as PropType<BadgeType>,
    default: 'default'
  },
  loading: {
    type: Boolean
  }
})

const badgeType = computed<BadgeType>(() =>
  props.loading ? 'loading' : props.type
)
</script>

<style lang="postcss" scoped>
.default {
  @apply bg-orange-50 text-orange-500;
}

.loading {
  @apply bg-emerald-50 text-emerald-500;
}
</style>
