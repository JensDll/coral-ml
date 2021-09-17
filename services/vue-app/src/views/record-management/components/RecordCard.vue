<template>
  <div class="border p-6 rounded-md">
    <div class="title-grid">
      <h3 class="title">{{ modelName }}</h3>
      <BaseBadge v-if="record.loaded" class="model-loaded">Loaded</BaseBadge>
      <LoadingIcon v-if="loading" class="loading" />
    </div>
    <div class="flex items-center justify-between">
      <div>
        <BaseButton
          class="px-6 py-1 rounded font-semibold"
          type="secondary"
          @click="handleLoad()"
          reverse
          :disabled="loading"
        >
          Load
        </BaseButton>
      </div>
      <DownloadIcon
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
import { computed, ref, PropType } from 'vue'
import { recordRepository, modelRepository, ApiRecord } from '~/api'
import BaseButton from '~/components/base/BaseButton.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'
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
  router.push({ name: window.onLoadLinks[props.record.recordType] })
  const response = await modelRepository.loadModel(props.record.id)
  console.log(response)
  if (response.success) {
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

<style lang="postcss" scoped>
.title {
  @apply font-semibold break-all;
  grid-area: title;
}

.loading {
  @apply w-4 h-4 ml-4 self-start mt-1 mr-1;
  grid-area: loading;
}

.model-loaded {
  @apply justify-self-start;
  grid-area: model-loaded;
}

.title-grid {
  @apply grid gap-y-2 mb-8;
  grid-template-columns: 1fr auto;
  grid-template-rows: auto auto;
  grid-template-areas:
    'title loading'
    'model-loaded model-loaded';
}

@screen lg {
  .title-grid {
    grid-template-columns: 1fr auto auto;
    grid-template-rows: auto;
    grid-template-areas: 'title model-loaded loading';
  }

  .model-loaded {
    @apply justify-self-end self-start ml-4;
  }
}
</style>
