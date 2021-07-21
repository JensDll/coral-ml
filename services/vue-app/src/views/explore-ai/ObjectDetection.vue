<template>
  <v-title title="Video Analysis"></v-title>
  <form class="w-1/2">
    <div>
      <label class="block" for="top-k">Show top k results</label>
      <input
        type="number"
        class="border py-2 px-4"
        v-model.number="formData.topK"
        id="top-k"
      />
    </div>
  </form>
  <canvas
    ref="videoCanvas"
    class="rounded-lg w-full lg:w-5/6 2xl:w-1/2 mt-8"
    v-show="!loading"
  ></canvas>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/BaseTitle.vue'
import type { UpdateVideoRequest } from '~/api'
import { socketService } from '~/api'

const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const formData: UpdateVideoRequest = reactive({
  topK: 1,
  threshold: 0.1
})

watch(formData, formData => {
  console.log(formData)
  socketService.updateVideo(formData)
})

let player: any

onMounted(() => {
  player = new JSMpeg.Player(import.meta.env.VITE_VIDEO_URI, {
    canvas: videoCanvas.value,
    disableWebAssembly: true,
    reconnectInterval: 0,
    onSourceEstablished() {
      loading.value = false
    }
  })
})

onBeforeUnmount(() => {
  player.source.socket.close()
})
</script>

<style lang="postcss" scoped></style>
