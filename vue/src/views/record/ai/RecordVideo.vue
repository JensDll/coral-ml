<template>
  <v-title title="Video Analysis"></v-title>
  <v-loading v-if="loading" />
  <canvas ref="videoCanvas" class="rounded-md" v-show="!loading"></canvas>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'
import VLoading from '~/components/base/VLoading.vue'

const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)

onMounted(() => {
  const player = new JSMpeg.Player(import.meta.env.VITE_VIDEO_URI, {
    canvas: videoCanvas.value,
    disableWebAssembly: true,
    onSourceEstablished() {
      loading.value = false
    }
  })
})
</script>

<style lang="postcss" scoped></style>
