<template>
  <div class="flex items-end mb-4">
    <base-title title="Image Classification" />
    <base-badge class="ml-4" v-if="recordStore.loadingRecord" loading>
      Loading Model
    </base-badge>
    <base-badge class="ml-4" v-else-if="recordLoaded">Loaded</base-badge>
  </div>
  <p v-if="recordLoaded && !recordStore.loadingRecord">
    {{ recordStore.loadedModelFileName }}
  </p>
  <classification-form class="mt-8" @submit="classify" :submitting="loading" />
  <div v-if="result" class="mt-16">
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
import { socketService } from '~/api'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'
import { useLoading } from '~/composable'
import { useRecordStore } from '~/store/recordStore'
import ClassificationForm from './components/ClassificationForm.vue'
import { computed } from '@vue/runtime-core'

const recordStore = useRecordStore()
const recordLoaded = computed(() => {
  return recordStore.loadedType === 'image'
})

const [[loading, result, classify]] = useLoading(
  socketService.classify.bind(socketService)
)
</script>

<style lang="postcss" scoped></style>
