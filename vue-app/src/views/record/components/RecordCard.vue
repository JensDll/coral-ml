<template>
  <div class="border p-6 rounded-md">
    <div class="flex justify-between items-start mb-8">
      <h3 class="font-semibold break-words w-3/5">{{ modelName }}</h3>
      <v-badge class="ml-4" v-if="record.loaded">Loaded</v-badge>
    </div>
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
        @click="recordRepository.download(record.id)"
        class="w-6 h-6 hover:text-blue-700 cursor-pointer"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { recordRepository, socketService } from '~/api'
import type { Record } from '~/api'
import VButton from '~/components/base/VButton.vue'
import VBadge from '~/components/base/VBadge.vue'
import { DownloadIcon } from '@heroicons/vue/outline'
import { useLoading } from '~/composable'
import { useRouter } from 'vue-router'

const loading = ref(false)

const props = defineProps({
  record: {
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
  (event: 'delete'): void
}>()

const router = useRouter()
const modelName = computed(() =>
  props.record.modelFileName.replace('.tflite', '')
)

async function handleLoad() {
  loading.value = true
  router.push({ name: props.onLoadLink })
  const success = await socketService.loadModel(props.record.id)
  loading.value = false
}

async function handleDelete() {
  await recordRepository.delete(false, props.record.id).promise
  emit('delete')
}
</script>

<style lang="postcss" scoped></style>
