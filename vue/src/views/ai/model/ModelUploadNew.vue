<template>
  <v-page-title
    title="Upload a new Model"
    @back="$router.back()"
    back
  ></v-page-title>
  <model-upload-form @submit="handleUpload" />
</template>

<script setup lang="ts">
import VPageTitle from '~/components/base/VPageTitle.vue'
import ModelUploadForm from './components/ModelUploadForm.vue'
import type { FormData } from './components/ModelUploadForm.vue'
import { modelRepository } from '~/api'
import { useRouter } from 'vue-router'

const router = useRouter()

async function handleUpload({ files }: FormData) {
  const idxModel = files[0].name.endsWith('.tflite') ? 0 : 1
  const model = files[idxModel]
  const label = files[Math.abs(1 - idxModel)]

  const { responseOk } = await modelRepository.uploadModel(model, label, false)
    .promise

  if (responseOk) {
    router.back()
  }
}
</script>

<style lang="postcss" scoped></style>
