<template>
  <div class="flex flex-col items-start lg:flex-row lg:items-center">
    <base-title title="Video Analysis" />
    <base-badge
      class="my-3 lg:ml-4 lg:my-0"
      v-if="recordStore.loadingRecord"
      loading
    >
      Loading Model
    </base-badge>
    <base-badge class="my-3 lg:ml-4 lg:my-0" v-else-if="recordLoaded">
      Loaded
    </base-badge>
  </div>
  <p
    v-if="recordLoaded && !recordStore.loadingRecord"
    class="break-all lg:mt-3"
  >
    {{ recordStore.loadedModelFileName }}
  </p>
  <form-top-k-controller
    v-if="recordLoaded"
    class="mt-8"
    v-model="formData.topK"
  />
  <canvas
    ref="videoCanvas"
    class="w-full mt-8 resize lg:w-auto"
    v-show="!loading && !recordStore.loadingRecord"
  ></canvas>
</template>

<script setup lang="ts">
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'
import FormTopKController from '~/components/form/FormTopKController.vue'

import { socketService } from '~/api'
import { useRecordStore } from '~/store/recordStore'
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import type { UpdateModelRequest } from '~/api'
import type { Ref } from 'vue'

const recordStore = useRecordStore()
const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const formData = reactive<UpdateModelRequest>({
  topK: 1,
  threshold: 0.1
})

const recordLoaded = computed(() => {
  return recordStore.loadedType === 'video'
})

socketService.updateVideo(formData)

watch(formData, formData => {
  const settings: UpdateModelRequest = {
    topK: typeof formData.topK !== 'number' ? 0 : formData.topK,
    threshold: typeof formData.threshold !== 'number' ? 0 : formData.threshold
  }
  socketService.updateVideo(settings)
})

let player: any

onMounted(() => {
  player = new JSMpeg.Player(import.meta.env.VITE_NODE_VIDEO, {
    audio: false,
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
