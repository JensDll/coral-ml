<template>
  <v-title title="Upload a new Model" @back="$router.back()" back />
  <p>A Coral Edge TPU model consists of a label and model file.</p>
  <p>Select both in the form field below and press upload.</p>
  <form-record-upload @submit="handleUpload" />
</template>

<script setup lang="ts">
import VTitle from '~/components/base/VTitle.vue'
import FormRecordUpload from './components/FormRecordUpload.vue'
import type { FormData } from './components/FormRecordUpload.vue'
import { recordRepository } from '~/api'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

async function handleUpload({ files }: FormData) {
  const idxModel = files[0].name.endsWith('.tflite') ? 0 : 1
  const model = files[idxModel]
  const label = files[Math.abs(1 - idxModel)]

  const { responseOk } = await recordRepository.upload(
    false,
    route.params.recordTypeId as string,
    model,
    label
  ).promise

  if (responseOk) {
    router.back()
  }
}
</script>

<style lang="postcss" scoped></style>
