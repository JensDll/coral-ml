<template>
  <div class="mb-8">
    <base-title :title="$route.params.recordType" @back="$router.back()" back />
  </div>
  <div v-if="loading">Loading ...</div>
  <base-card-grid class="gap-12 items-start" v-else>
    <record-card
      v-for="record in recordStore.records"
      :key="record.id"
      :record="record"
    ></record-card>
  </base-card-grid>
</template>

<script setup lang="ts">
import { recordRepository } from '~/api'
import RecordCard from './components/RecordCard.vue'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import { useRecordStore } from '~/store/recordStore'
import { useRoute } from 'vue-router'
import { useLoading } from '~/composable'

const recordStore = useRecordStore()
const route = useRoute()

const [[loading, , loadWithRecordTypeId]] = useLoading(
  recordRepository.loadWithRecordTypeId
)
loadWithRecordTypeId(route.params.recordTypeId as string)
</script>

<style lang="postcss" scoped></style>
