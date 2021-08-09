<template>
  <div class="flex items-end mb-4">
    <base-title title="Video Analysis" />
    <base-badge class="ml-4" v-if="recordStore.loadingRecord" loading>
      Loading Model
    </base-badge>
    <base-badge class="ml-4" v-else-if="recordLoaded">Loaded</base-badge>
  </div>
  <p v-if="recordLoaded && !recordStore.loadingRecord">
    {{ recordStore.loadedModelFileName }}
  </p>
  <form v-if="recordLoaded" class="w-1/2 mt-8">
    <div>
      <label class="block font-semibold mb-2 rounded-md" for="top-k">
        Show Top Results
      </label>
      <input
        type="number"
        class="border py-2 px-4"
        min="0"
        v-model.number="formData.topK"
        id="top-k"
      />
    </div>
  </form>
  <canvas
    ref="videoCanvas"
    class="rounded-lg w-full lg:w-5/6 2xl:w-4/6 mt-8"
    v-show="!loading && !recordStore.loadingRecord"
  ></canvas>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import type { Ref } from 'vue'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'

import type { UpdateVideoRequest } from '~/api'
import { socketService } from '~/api'
import { useRecordStore } from '~/store/recordStore'

const recordStore = useRecordStore()
const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const formData: UpdateVideoRequest = reactive({
  topK: 1,
  threshold: 0.1
})

const recordLoaded = computed(() => {
  return recordStore.loadedType === 'video'
})

socketService.updateVideo(formData)

watch(formData, formData => {
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
