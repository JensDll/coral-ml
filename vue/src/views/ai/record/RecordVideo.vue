<template>
  <v-title title="Video Analysis"></v-title>
  <!-- <img
    src="http://localhost:5000/video"
    alt="stream"
    ref="imgRef"
    class="rounded-2xl"
  /> -->
  <video ref="videoRef" class="rounded-2xl"></video>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'
import { useSocketService } from '~/composable/useSocketService'
import Hls from 'hls.js'

const videoRef = ref() as Ref<HTMLVideoElement>

onMounted(() => {
  if (Hls.isSupported()) {
    console.log(Hls.version)
    const hls = new Hls()
    hls.attachMedia(videoRef.value)
    hls.on(Hls.Events.MEDIA_ATTACHED, () => {
      console.log('Video and hls.js are now bound together!')
      hls.loadSource('http://127.0.0.1:8080/live/livestream.m3u8')
      hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
        console.log(
          'manifest loaded, found ' + data.levels.length + ' quality level'
        )
        videoRef.value.play()
      })
    })
  }
})

// const imgRef = ref() as Ref<HTMLImageElement>

// const socketService = useSocketService()

// socketService.readVideo(imgRef)
</script>

<style lang="postcss" scoped></style>
