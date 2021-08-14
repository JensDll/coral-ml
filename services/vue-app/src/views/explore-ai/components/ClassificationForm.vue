<template>
  <form class="lg:w-1/2" @submit.prevent="handleSubmit()" v-bind="$attrs">
    <form-file-upload
      label="Image File"
      v-model="form.images.$value"
      :errors="form.images.$errors"
      @input="form.images.$onBlur()"
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
    </div>
  </form>
  <form-top-k-controller
    class="mt-12 sticky top-24 z-10"
    v-model="formData.topK"
  />
</template>

<script setup lang="ts">
import { useValidation, Field } from 'vue3-form-validation'
import VButton from '~/components/base/BaseButton.vue'
import FormTopKController from '~/components/form/FormTopKController.vue'
import FormFileUpload from '~/components/form/FormFileUpload.vue'
import { minMax } from '~/utils'
import { reactive, watch } from 'vue'
import {
  UpdateModelRequest,
  socketService,
  MessageEnvelope,
  ClassificationResult
} from '~/api'

const props = defineProps({
  submitting: {
    type: Boolean
  }
})

const emit = defineEmits<{
  (event: 'submit', image: File): void
  (event: 'updateSettings', result: ClassificationResult): void
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

const formData = reactive<UpdateModelRequest>({
  topK: 5,
  threshold: 0.1
})

socketService.updateclassify(formData)

watch(formData, async formData => {
  const settings: UpdateModelRequest = {
    topK: typeof formData.topK !== 'number' ? 0 : formData.topK,
    threshold: typeof formData.threshold !== 'number' ? 0 : formData.threshold
  }
  const result = await socketService.updateclassify(settings)
  if (result.success) {
    emit('updateSettings', result)
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
