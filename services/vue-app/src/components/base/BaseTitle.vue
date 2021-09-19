<template>
  <h1 class="flex items-center text-2xl lg:text-3xl font-extrabold">
    <ArrowLeftIcon
      v-if="back"
      class="w-6 h-6 mr-4 hover:text-blue-700 cursor-pointer"
      @click="$emit('back')"
    />
    {{ title }}
  </h1>
</template>

<script lang="ts" setup>
import { ArrowLeftIcon } from '@heroicons/vue/outline'

defineProps({
  title: {
    type: String,
    required: true
  },
  back: {
    type: Boolean
  }
})

defineEmits(['back'])
</script>

<style lang="postcss" scoped></style>
