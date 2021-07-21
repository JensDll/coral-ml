<template>
  <div
    :class="['rounded-md font-medium py-1 px-4 flex items-center', badgeType]"
  >
    <slot></slot>
    <loading-icon class="ml-4 w-4 h-4" v-if="loading" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from '@vue/runtime-core'
import LoadingIcon from '../icons/LoadingIcon.vue'

type BadgeType = 'loading' | 'default'

export default defineComponent({
  components: {
    LoadingIcon
  },
  props: {
    type: {
      type: String as PropType<BadgeType>,
      default: 'default'
    },
    loading: {
      type: Boolean
    }
  },
  computed: {
    badgeType(): BadgeType {
      return this.loading ? 'loading' : this.type
    }
  }
})
</script>

<style lang="postcss" scoped>
.default {
  @apply bg-orange-50 text-orange-500;
}

.loading {
  @apply bg-emerald-50 text-emerald-500;
}
</style>
