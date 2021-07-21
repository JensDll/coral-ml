<template>
  <div class="border p-6 rounded-md">
    <div class="flex justify-between items-start mb-8">
      <h3 class="font-semibold break-words w-3/5">{{ modelName }}</h3>
      <div class="ml-8 flex items-center">
        <v-badge v-if="record.loaded">Loaded</v-badge>
        <loading-icon
          v-if="loading"
          class="w-4 mr-1 h-4 ml-4"
          :class="{ 'mt-1': !record.loaded }"
        />
      </div>
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
        @click="handleDownload()"
        class="w-6 h-6 hover:text-blue-700 cursor-pointer"
        :class="{
          'opacity-40 cursor-not-allowed pointer-events-none': loading
        }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { recordRepository, socketService } from '~/api'
import type { ApiRecord } from '~/api'
import VButton from '~/components/base/BaseButton.vue'
import VBadge from '~/components/base/BaseBadge.vue'
import { DownloadIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import LoadingIcon from '~/components/icons/LoadingIcon.vue'
import { useRecordStore } from '~/store/recordStore'

const router = useRouter()
const recordStore = useRecordStore()

const loading = ref(false)

const props = defineProps({
  record: {
    type: Object as PropType<ApiRecord>,
    required: true
  },
  loaded: {
    type: Boolean
  }
})

const modelName = computed(() =>
  props.record.modelFileName.replace('.tflite', '')
)

async function handleLoad() {
  loading.value = true
  recordStore.loadingRecord = true
  router.push({ name: window.onLoadLinks[props.record.recordTypeId] })
  const success = await socketService.loadModel(props.record.id)
  if (success) {
    await recordRepository.loadLoaded()
  }
  recordStore.loadingRecord = false
  loading.value = false
}

async function handleDelete() {
  loading.value = true
  await recordRepository.delete(false, props.record.id).promise
  await recordRepository.loadWithRecordTypeId(props.record.recordTypeId)
  loading.value = false
}

async function handleDownload() {
  loading.value = true
  await recordRepository.download(props.record.id)
  loading.value = false
}
</script>

<style lang="postcss" scoped></style>
