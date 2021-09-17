<template>
  <form class="lg:w-1/2" @submit.prevent="handleSubmit()" v-bind="$attrs">
    <FormFileUpload
      label="Image File"
      v-model="form.images.$value"
      :errors="form.images.$errors"
      @input="form.images.$onBlur()"
      image
      accept=".jpg, .jpeg, .png"
    ></FormFileUpload>
    <div class="mt-8">
      <BaseButton
        class="font-semibold px-6 py-2 rounded"
        html-type="submit"
        :loading="submitting"
      >
        Run Classification
      </BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useValidation, Field } from 'vue3-form-validation'
import { minMax } from '~/utils'
import BaseButton from '~/components/base/BaseButton.vue'
import FormFileUpload from '~/components/form/FormFileUpload.vue'

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

const { form, formFields, validateFields } = useValidation<Data>({
  images: {
    $value: [],
    $rules: [minMax(1, 1)('Please select an image')]
  }
})

const handleSubmit = async () => {
  try {
    const { images } = await validateFields()
    emit('submit', images[0])
  } catch {
  } finally {
    for (const formField of formFields.value.values()) {
      formField.touched = false
    }
  }
}
</script>

<style lang="postcss" scoped></style>
