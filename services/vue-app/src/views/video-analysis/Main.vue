<template>
  <div class="flex flex-col items-start lg:flex-row lg:items-center">
    <BaseTitle title="Video Analysis" />
    <BaseBadge
      class="my-3 lg:ml-4 lg:my-0"
      v-if="recordStore.loadingRecord"
      loading
    >
      Loading Model
    </BaseBadge>
    <BaseBadge class="my-3 lg:ml-4 lg:my-0" v-else-if="recordLoaded">
      Loaded
    </BaseBadge>
  </div>
  <p
    v-if="recordLoaded && !recordStore.loadingRecord"
    class="break-all lg:mt-3"
  >
    {{ recordStore.loadedModelFileName }}
  </p>
  <FormPlusMinusInput
    v-if="recordLoaded"
    class="mt-8"
    v-model="settings.topK"
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
import FormPlusMinusInput from '~/components/form/FormPlusMinusInput.vue'

import { videoRepository, VideoSettings } from '~/api'
import { useRecordStore } from '~/store/recordStore'
import {
  computed,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref,
  watch,
  Ref
} from 'vue'

const recordStore = useRecordStore()
const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const settings = reactive<VideoSettings>({
  topK: 1,
  scoreThreshold: 0.1
})

const recordLoaded = computed(() => {
  return recordStore.loadedType === 'video'
})

videoRepository.updateSettings(settings)

watch(settings, settings => {
  videoRepository.updateSettings(settings)
})

let player: any

onMounted(() => {
  player = new JSMpeg.Player(import.meta.env.VITE_URI_NODE_VIDEO, {
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
