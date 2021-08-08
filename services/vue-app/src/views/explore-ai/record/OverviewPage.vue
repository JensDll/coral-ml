<template>
  <div class="mb-8">
    <base-title :title="`Models`" @back="$router.back()" back />
    <div class="mt-2 text-xl">{{ $route.params.recordType }}</div>
  </div>
  <base-card-grid class="gap-12">
    <record-card
      v-for="record in recordStore.records"
      :key="record.id"
      :record="record"
    ></record-card>
  </base-card-grid>
</template>

<script lang="ts">
import { recordRepository } from '~/api'
import RecordCard from './components/RecordCard.vue'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import { defineComponent } from 'vue'
import { useRecordStore } from '~/store/recordStore'

export default defineComponent({
  components: {
    RecordCard,
    BaseTitle,
    BaseCardGrid
  },
  setup() {
    const recordStore = useRecordStore()
    return {
      recordStore
    }
  },
  async beforeRouteEnter(to, from, next) {
    await recordRepository.loadWithRecordTypeId(
      to.params.recordTypeId as string
    )
    next()
  }
})
</script>

<style lang="postcss" scoped></style>
