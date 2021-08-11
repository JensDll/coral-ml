<template>
  <div class="mb-8">
    <v-title title="Upload a new Model" @back="$router.back()" back />
  </div>
  <p class="2xl:w-2/3">
    Upload a Coral Edge TPU model. For Classifcation tasks this consists of
    TFLite and Label file. Select one or both in the form field below and press
    upload.
  </p>
  <record-upload-form @submit="handleUpload" class="mt-8" />
</template>

<script setup lang="ts">
import VTitle from '~/components/base/BaseTitle.vue'
import RecordUploadForm from './components/RecordUploadForm.vue'
import type { FormData } from './components/RecordUploadForm.vue'
import { recordRepository, recordTypeRepository } from '~/api'
import { useRouter, useRoute } from 'vue-router'
import { useRecordStore } from '~/store/recordStore'

const router = useRouter()
const route = useRoute()
const recordTypeId = route.params.recordTypeId as string

async function handleUpload({ files }: FormData) {
  const idxModel = files[0].name.endsWith('.tflite') ? 0 : 1
  const model = files[idxModel]
  const label = files[Math.abs(1 - idxModel)]

  router.back()

  await recordRepository.upload(false, recordTypeId, model, label).promise
  await Promise.all([
    recordRepository.loadWithRecordTypeId(recordTypeId),
    recordTypeRepository.loadAll()
  ])
}
</script>

<style lang="postcss" scoped></style>
