<template>
  <div>
    <label class="block font-semibold mb-2 rounded-md" for="top-k">
      Show Top Results
    </label>
    <div class="flex items-center">
      <plus-circle-icon
        v-long-press="increaseTopK"
        class="
          w-8
          h-8
          text-blue-500
          cursor-pointer
          hover:text-blue-700
          fill-white
        "
        @mousedown="increaseTopK()"
        @touchstart.prevent="increaseTopK()"
      />
      <input
        id="top-k"
        type="number"
        min="0"
        v-model="topK"
        class="input-number-reset w-16 px-2 py-1 mx-2"
      />
      <minus-circle-icon
        class="
          w-8
          h-8
          text-red-500
          cursor-pointer
          hover:text-red-700
          test
          fill-white
        "
        v-long-press="decreaseTopK"
        @mousedown="decreaseTopK()"
        @touchstart.prevent="decreaseTopK()"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  }
})

const topK = computed<number>({
  get() {
    return props.modelValue
  },
  set(topK: string | number) {
    emit('update:modelValue', typeof topK === 'string' ? 0 : topK)
  }
})

const emit = defineEmits<{
  (event: 'update:modelValue', topK: number): void
}>()

const increaseTopK = () => {
  topK.value++
}

const decreaseTopK = () => {
  if (props.modelValue !== 0) {
    topK.value--
  }
}
</script>

<style lang="postcss" scoped></style>
