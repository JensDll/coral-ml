<template>
  <v-title title="Image Classification" />
  <classification-form @submit="classify" :submitting="loading" />
  <pre v-if="result">{{ result }}</pre>
</template>

<script setup lang="ts">
import { socketService } from '~/api'
import VTitle from '~/components/base/BaseTitle.vue'
import { useLoading } from '~/composable'
import ClassificationForm from './components/ClassificationForm.vue'

const [[loading, result, classify]] = useLoading(
  socketService.classify.bind(socketService)
)
</script>

<style lang="postcss" scoped></style>
