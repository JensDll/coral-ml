<template>
  <form class="lg:w-1/2" @submit.prevent="handleSubmit()">
    <form-file-upload
      label="Image File"
      v-model="form.images.$value"
      :errors="form.images.$errors"
      image
      accept=".jpg, .jpeg, .png"
    ></form-file-upload>
    <div class="mt-8">
      <v-button
        class="font-semibold px-6 py-2 rounded"
        html-type="submit"
        :disabled="submitting"
      >
        Run Classification
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
import { useValidation } from 'vue3-form-validation'
import type { Field } from 'vue3-form-validation'
import VButton from '~/components/base/BaseButton.vue'
import FormFileUpload from '~/components/form/FormFileUpload.vue'
import { minMax } from '~/utils'

const props = defineProps({
  submitting: {
    type: Boolean
  }
})

const emit = defineEmits<{
  (event: 'submit', image: File): void
}>()

type Data = {
  images: Field<File[]>
}

const { form, validateFields, resetFields } = useValidation<Data>({
  images: {
    $value: [],
    $rules: [minMax(1, 1)('Please select an image')]
  }
})

const handleSubmit = async () => {
  try {
    const { images } = await validateFields()
    emit('submit', images[0])
  } catch {}
}
</script>

<style lang="postcss" scoped></style>
