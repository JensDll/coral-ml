<template>
  <form class="lg:w-1/2" @submit.prevent="handleSubmit()">
    <form-file-upload
      label="Model and Label File"
      v-model="form.files.$value"
      :errors="form.files.$errors"
      multiple
    >
      <template #hint>
        <p class="text-gray-500 text-xs">TFLITE + Label File</p>
      </template>
    </form-file-upload>
    <div class="mt-8">
      <v-button class="font-semibold px-6 py-2 rounded" html-type="submit">
        Upload
      </v-button>
      <v-button
        class="font-semibold px-6 py-2 rounded ml-4"
        type="basic"
        @click="resetFields()"
      >
        Cancel
      </v-button>
    </div>
  </form>
</template>

<script setup lang="ts">
import FormFileUpload from "~/components/form/FormFileUpload.vue"
import VButton from "~/components/base/VButton.vue"
import { useValidation } from "vue3-form-validation"
import type { Field } from "vue3-form-validation"
import type { PlainFormData } from "~/utils"

export type FormData = PlainFormData<typeof validateFields>

type Data = {
  files: Field<File[]>
}

const { form, validateFields, resetFields } = useValidation<Data>({
  files: {
    $value: [],
    $rules: [
      files => {
        if (
          files.length !== 2 ||
          !files.find(f => f.name.endsWith(".tflite"))
        ) {
          return "Please select a model and label file"
        }
      }
    ]
  }
})

const emit = defineEmits<{
  (event: "submit", formData: FormData): void
}>()

const handleSubmit = async () => {
  try {
    const formData = await validateFields()
    emit("submit", formData)
  } catch {}
}
</script>

<style lang="postcss"></style>
