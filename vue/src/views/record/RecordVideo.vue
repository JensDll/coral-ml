<template>
  <v-title title="Video Analysis"></v-title>
  <canvas ref="videoCanvas"></canvas>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'

const videoCanvas = ref() as Ref<HTMLCanvasElement>

onMounted(() => {
  const player = new JSMpeg.Player(import.meta.env.VITE_VIDEO_URI, {
    canvas: videoCanvas.value,
    disableWebAssembly: true
  })
})
</script>

<style lang="postcss" scoped></style>
