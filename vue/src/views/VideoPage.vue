<template>
  <h1 class="text-3xl font-extrabold mb-8">Video Analysis</h1>
  <v-model-form />
  <img src="" ref="imgRef" />
</template>

<script setup lang="ts">
import { ref } from "vue"
import type { Ref } from "vue"
import { useSockerService } from "../api"
import VModelForm from "../components/form/VModelForm.vue"

// const imgRef = ref() as Ref<HTMLImageElement>

// const socketService = useSockerService()
// socketService.readVideo(imgRef)
</script>

<style lang=""></style>
