<template>
  <v-title title="Upload a new Model" @back="$router.back()" back />
  <p>A Coral Edge TPU model consists of a label and model file.</p>
  <p>Select both in the form field below and press upload.</p>
  <record-upload-form @submit="handleUpload" class="mt-8" />
</template>

<script setup lang="ts">
import VTitle from '~/components/base/BaseTitle.vue'
import RecordUploadForm from './components/RecordUploadForm.vue'
import type { FormData } from './components/RecordUploadForm.vue'
import { recordRepository } from '~/api'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

async function handleUpload({ files }: FormData) {
  const idxModel = files[0].name.endsWith('.tflite') ? 0 : 1
  const model = files[idxModel]
  const label = files[Math.abs(1 - idxModel)]

  router.back()

  await recordRepository.upload(
    false,
    route.params.recordTypeId as string,
    model,
    label
  ).promise
}
</script>

<style lang="postcss" scoped></style>
