<template>
  <div class="mb-8">
    <base-title :title="$route.params.recordType" @back="$router.back()" back />
  </div>
  <base-card-grid class="gap-12 items-start">
    <template v-if="loading">
      <base-skeleton v-for="i in 3" :key="i">
        <div class="w-full h-5 skeleton-item"></div>
        <div class="w-3/4 h-5 mt-3 skeleton-item"></div>
        <div class="w-1/2 h-7 mt-8 skeleton-item"></div>
      </base-skeleton>
      <div></div>
    </template>
    <template v-else>
      <record-card
        v-for="record in recordStore.records"
        :key="record.id"
        :record="record"
      ></record-card>
    </template>
  </base-card-grid>
</template>

<script setup lang="ts">
import RecordCard from './components/RecordCard.vue'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import BaseSkeleton from '~/components/base/BaseSkeleton.vue'

import { recordRepository } from '~/api'
import { useRecordStore } from '~/store/recordStore'
import { useRoute } from 'vue-router'
import { useLoading } from '~/composition'

const recordStore = useRecordStore()
const route = useRoute()

const [[loading, , loadWithRecordTypeId]] = useLoading(
  recordRepository.loadWithRecordTypeId
)
loadWithRecordTypeId(route.params.recordTypeId as string)
</script>

<style lang="postcss" scoped></style>
