<template>
  <div class="mb-8">
    <base-title :title="$route.params.recordType" @back="$router.back()" back />
  </div>
  <base-card-grid class="gap-12">
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

const recordStore = useRecordStore()
const route = useRoute()
recordRepository.loadWithRecordTypeId(route.params.recordTypeId as string)
</script>

<style lang="postcss" scoped></style>
