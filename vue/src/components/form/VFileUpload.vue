<template>
  <label>
    <div class="flex justify-between font-semibold mb-3">
      {{ label }}
    </div>
    <div
      class="
        group
        border-2 border-dashed border-emerald-300
        rounded-sm
        py-20
        flex
        justify-center
        items-center
        relative
      "
      :class="{ 'bg-red-50 border-red-300': hasError }"
    >
      <input
        class="group w-full h-full absolute opacity-0 cursor-pointer"
        type="file"
        multiple
        @change="handleChange"
      />
      <div class="text-center">
        <p>
          <span
            class="text-indigo-500 font-semibold group-hover:text-indigo-400"
            :class="{ 'text-red-500 group-hover:text-red-400': hasError }"
          >
            Upload a file
          </span>
          or drag and drop
        </p>
      </div>
    </div>
  </label>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits, ref } from "vue"

defineProps({
  label: {
    type: String,
    default: "Image"
  },
  hasError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["upload"])

const files = ref<File | null>(null)

// const setFile = (value: File | null) => {
//   file.value = value
//   emit("upload", value)
// }
const handleChange = (e: Event) => {
  const input = e.target as HTMLInputElement
  console.log(input.files)
}
</script>
