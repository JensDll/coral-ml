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
  <form v-if="recordLoaded" class="w-1/2 mt-8">
    <div>
      <label class="block font-semibold mb-2 rounded-md" for="top-k">
        Show Top Results
      </label>
      <div class="flex items-center">
        <plus-circle-icon
          v-long-press="increaseTopK"
          class="w-8 h-8 text-blue-500 cursor-pointer hover:text-blue-700"
          @mousedown="increaseTopK()"
          @touchstart.prevent="increaseTopK()"
        />
        <input
          id="top-k"
          ref="topK"
          type="number"
          min="0"
          v-model="formData.topK"
          class="input-number-reset w-16 px-2 py-1 mx-2"
        />
        <minus-circle-icon
          class="w-8 h-8 text-red-500 cursor-pointer hover:text-red-700"
          v-long-press="decreaseTopK"
          @mousedown="decreaseTopK()"
          @touchstart.prevent="decreaseTopK()"
        />
      </div>
    </div>
  </form>
  <canvas
    ref="videoCanvas"
    class="rounded-lg w-full lg:w-5/6 2xl:w-4/6 mt-8"
    v-show="!loading && !recordStore.loadingRecord"
  ></canvas>
</template>

<script setup lang="ts">
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'
import { PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
import { socketService } from '~/api'
import { useRecordStore } from '~/store/recordStore'
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import type { UpdateVideoRequest } from '~/api'
import type { Ref } from 'vue'

const recordStore = useRecordStore()
const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const formData: UpdateVideoRequest = reactive({
  topK: 1,
  threshold: 0.1
})
const topKInput = ref<HTMLInputElement>()

const recordLoaded = computed(() => {
  return recordStore.loadedType === 'video'
})

socketService.updateVideo(formData)

watch(formData, formData => {
  socketService.updateVideo(formData)
})

const increaseTopK = () => {
  formData.topK++
}

const decreaseTopK = () => {
  if (formData.topK !== 0) {
    formData.topK--
  }
}

let player: any

onMounted(() => {
  player = new JSMpeg.Player(import.meta.env.VITE_VIDEO_URI, {
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
