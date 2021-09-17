<template>
  <form class="lg:w-1/2" @submit.prevent="handleSubmit()">
    <FormFileUpload
      label="Model and Label File For Classifcation"
      v-model="form.files.$value"
      :errors="form.files.$errors"
      multiple
    >
      <template #hint>
        <p class="text-gray-500 text-xs">TFLite + Optional Label File</p>
      </template>
    </FormFileUpload>
    <div class="mt-8">
      <BaseButton class="font-semibold px-6 py-2 rounded" html-type="submit">
        Upload
      </BaseButton>
      <BaseButton
        class="font-semibold px-6 py-2 rounded ml-4"
        type="basic"
        @click="resetFields()"
      >
        Cancel
      </BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import FormFileUpload from '~/components/form/FormFileUpload.vue'
import BaseButton from '~/components/base/BaseButton.vue'
import { useValidation, Field } from 'vue3-form-validation'
import { PlainFormData } from '~/utils'

export type FormData = PlainFormData<typeof validateFields>

type Data = {
  files: Field<File[]>
}

const { form, validateFields, resetFields } = useValidation<Data>({
  files: {
    $value: [],
    $rules: [
      files => {
        if (!files.find(f => f.name.endsWith('.tflite'))) {
          return 'Please select one model file'
        }
      }
    ]
  }
})

const emit = defineEmits<{
  (event: 'submit', formData: FormData): void
}>()

const handleSubmit = async () => {
  try {
    const formData = await validateFields()
    emit('submit', formData)
  } catch {}
}
</script>

<style lang="postcss"></style>
