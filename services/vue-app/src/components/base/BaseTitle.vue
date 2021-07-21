<template>
  <h1 class="flex items-center text-3xl font-extrabold">
    <ArrowLeftIcon
      v-if="back"
      class="w-6 h-6 mr-4 hover:text-blue-700 cursor-pointer"
      @click="$emit('back')"
    />
    {{ title }}
  </h1>
</template>

<script lang="ts">
import { ArrowLeftIcon } from '@heroicons/vue/outline'
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
  name: 'vtitle',
  emits: ['back'],
  components: {
    ArrowLeftIcon
  },
  props: {
    title: {
      type: String,
      required: true
    },
    back: {
      type: Boolean
    }
  }
})
</script>

<style lang="postcss" scoped></style>
