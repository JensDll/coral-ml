<template>
  <div class="border p-6 rounded-md">
    <h3 class="break-words font-semibold mb-8">{{ modelName }}</h3>
    <div class="flex items-center justify-between">
      <div>
        <v-button
          class="px-3 py-1 rounded font-semibold"
          type="secondary"
          @click="handleLoad()"
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
          @click="handleDelete()"
        >
          Delete
        </v-button>
      </div>
      <download-icon
        @click="recordRepository.download(model.id)"
        class="w-6 h-6 hover:text-blue-700 cursor-pointer"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { recordRepository } from '~/api'
import type { Record } from '~/api'
import VButton from '~/components/base/VButton.vue'
import { DownloadIcon } from '@heroicons/vue/outline'
import { useLoading, useSocketService } from '~/composable'
import { useRouter } from 'vue-router'

const loading = ref(false)

const props = defineProps({
  model: {
    type: Object as PropType<Record>,
    required: true
  },
  loaded: {
    type: Boolean
  },
  onLoadLink: {
    type: String
  }
})

const emit = defineEmits<{
  (event: 'load', id: number): void
  (event: 'delete', id: number): void
}>()

const router = useRouter()
const modelName = computed(() =>
  props.model.modelFileName.replace('.tflite', '')
)

const socketService = useSocketService()

async function handleLoad() {
  const success = await socketService.loadModel(props.model.id)
  if (success) {
    router.push({ name: props.onLoadLink })
  }
}

function handleDelete() {}
</script>

<style lang="postcss" scoped></style>
