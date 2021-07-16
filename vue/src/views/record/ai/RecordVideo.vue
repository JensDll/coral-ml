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
      <div class="flex text-white font-semibold cursor-pointer">
        <div class="bg-blue-500 pl-6 pr-3 py-2 rounded-tl-xl rounded-bl-xl">
          <minus-icon class="w-5 h-5" />
        </div>
        <div class="bg-blue-500 pr-6 pl-3 py-2 rounded-tr-xl rounded-br-xl">
          <plus-icon class="w-5 h-5" />
        </div>
      </div>
    </div>
  </form>
  <canvas ref="videoCanvas" class="rounded-lg w-4/6" v-show="!loading"></canvas>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'
import VLoading from '~/components/base/VLoading.vue'
import type { UpdateVideoRequest } from '~/api'
import { socketService } from '~/api'
import { PlusIcon, MinusIcon } from '@heroicons/vue/solid'

const videoCanvas = ref() as Ref<HTMLCanvasElement>
const loading = ref(true)
const formData: UpdateVideoRequest = reactive({
  topK: 5,
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
