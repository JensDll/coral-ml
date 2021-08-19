<template>
  <div class="flex flex-col items-start lg:flex-row lg:items-center">
    <base-title title="Image Classification" />
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
  <classification-form class="mt-10" @submit="classify" :submitting="loading" />
  <div class="sticky mt-6 z-10 top-k">
    <form-top-k-controller
      v-model="formData.topK"
      class="relative bg-white py-6 bg-opacity-90"
    />
    <!-- <div class="absolute h-24 w-full bg-gradient-to-b from-white-90"></div> -->
  </div>
  <div v-if="result" class="mt-10">
    <pre v-if="!result.success">{{ result.errors }}</pre>
    <template v-if="result.success" class="">
      <div class="font-semibold">Inference Time</div>
      <p class="font-mono mb-4">
        {{ result.data.inferenceTime.toFixed(2) }} ms
      </p>
    </template>
    <table v-if="result.success" class="table-fixed text-left w-full lg:w-3/4">
      <thead>
        <tr>
          <th class="w-8/12 pr-4 font-semibold">Classname</th>
          <th class="font-semibold">Probability</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in result.data.classes.length" :key="i">
          <td class="pr-4">{{ result.data.classes[i - 1] }}</td>
          <td class="font-mono">
            {{ result.data.probabilities[i - 1].toFixed(2).padStart(6, '0') }} %
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'
import ClassificationForm from './components/ClassificationForm.vue'
import FormTopKController from '~/components/form/FormTopKController.vue'

import { useLoading } from '~/composable'
import { useRecordStore } from '~/store/recordStore'
import { socketService, UpdateModelRequest } from '~/api'
import { computed, reactive, watch } from 'vue'

const recordStore = useRecordStore()
const recordLoaded = computed(() => {
  return recordStore.loadedType === 'image'
})

const [[loading, result, classify]] = useLoading(
  socketService.classify.bind(socketService)
)

const formData = reactive<UpdateModelRequest>({
  topK: 5,
  threshold: 0.1
})

socketService.updateClassify(formData)

watch(formData, async formData => {
  const settings: UpdateModelRequest = {
    topK: typeof formData.topK !== 'number' ? 0 : formData.topK,
    threshold: typeof formData.threshold !== 'number' ? 0 : formData.threshold
  }
  const classificationResult = await socketService.updateClassify(settings)
  result.value = classificationResult
})
</script>

<style lang="postcss" scoped>
.top-k {
  top: 73px;
}
</style>
