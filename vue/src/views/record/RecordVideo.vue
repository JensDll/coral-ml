<template>
  <v-title title="Video Analysis"></v-title>
  <video ref="video" class="rounded-2xl"></video>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'
import Hls from 'hls.js'

const video = ref() as Ref<HTMLVideoElement>

onMounted(() => {
  if (Hls.isSupported()) {
    const hls = new Hls()
    hls.attachMedia(video.value)
    hls.on(Hls.Events.MEDIA_ATTACHED, () => {
      console.log('Video and hls.js are now bound together!')
      hls.loadSource('http://localhost:8080/live/coral.m3u8')
      hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
        console.log(
          `Manifest loaded, found ${data.levels.length} quality level`
        )
        video.value.play()
      })
    })

    hls.on(Hls.Events.ERROR, function (event, data) {
      const errorType = data.type
      const errorDetails = data.details
      const errorFatal = data.fatal
      console.log(`Hls error ${errorType}, ${errorDetails}, ${errorFatal}`)
    })
  }
})
</script>

<style lang="postcss" scoped></style>
