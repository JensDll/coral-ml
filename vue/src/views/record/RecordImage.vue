<template>
  <v-title title="Image Classification" />
  <form-classification @submit="classify" :submitting="loading" />
  <pre v-if="result">{{ result }}</pre>
</template>

<script setup lang="ts">
import VTitle from '~/components/base/VTitle.vue'
import { useLoading, useSocketService } from '~/composable'
import FormClassification from './components/FormClassification.vue'

const socketService = useSocketService()

const [[loading, result, classify]] = useLoading(
  socketService.classify.bind(socketService)
)
</script>

<style lang="postcss" scoped></style>
