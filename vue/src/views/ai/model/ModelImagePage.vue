<template>
  <v-page-title title="Image Classification"></v-page-title>
  <image-classification-form @submit="handleSubmit" />
</template>

<script setup lang="ts">
import VPageTitle from '~/components/base/VPageTitle.vue'
import { useSocketService } from '~/composable'
import ImageClassificationForm from './components/ImageClassificationForm.vue'

const socketService = useSocketService()

async function handleSubmit(image: File) {
  const resp = await socketService.imageClassification(image)
  console.log(resp)
}
</script>

<style lang="postcss" scoped></style>
