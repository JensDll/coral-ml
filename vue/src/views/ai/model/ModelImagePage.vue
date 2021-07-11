<template>
  <v-page-title title="Image Classification"></v-page-title>
  <image-classification-form @submit="handleSubmit" />
</template>

<script setup lang="ts">
import VPageTitle from "~/components/base/VPageTitle.vue"
import { useSocketService } from "~/composable/useSocketService"
import ImageClassificationForm from "./components/ImageClassificationForm.vue"

const socketService = useSocketService()

async function handleSubmit(image: File) {
  await socketService.imageClassification(image)
}
</script>

<style lang="postcss" scoped></style>
