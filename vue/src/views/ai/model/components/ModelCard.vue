<template>
  <div class="border p-6 rounded-md">
    <h3 class="break-words font-semibold mb-8">{{ modelName }}</h3>
    <div class="flex items-center justify-between">
      <div>
        <v-button
          class="px-3 py-1 rounded font-semibold"
          type="secondary"
          @click="load()"
          reverse
          :disabled="loading"
        >
          Load
        </v-button>
        <v-button
          class="px-3 py-1 rounded font-semibold ml-4"
          type="danger"
          reverse
          :disabled="loading"
        >
          Delete
        </v-button>
      </div>
      <DownloadIcon
        @click="download()"
        class="w-6 h-6 hover:text-blue-700 cursor-pointer"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PropType } from 'vue'
import { modelRepository } from '~/api'
import type { TFLiteModelRecord } from '~/api'
import VButton from '~/components/base/VButton.vue'
import { DownloadIcon } from '@heroicons/vue/outline'
import { useDownload, useLoading, useSocketService } from '~/composable'
import { useRouter } from 'vue-router'

const props = defineProps({
  model: {
    type: Object as PropType<TFLiteModelRecord>,
    required: true
  }
})

const router = useRouter()
const modelName = computed(() => props.model.modelName.replace('.tflite', ''))

const socketService = useSocketService()

const [[loading, loadModel]] = useLoading(
  socketService.loadModel.bind(socketService)
)

async function load() {
  const resp = await loadModel(props.model.id)
  router.push({ name: 'image' })
}

async function download() {
  const { data } = await modelRepository.download(props.model.id, false).promise
  if (data) {
    useDownload(data, 'model.zip')
  }
}
</script>

<style lang="postcss" scoped></style>
