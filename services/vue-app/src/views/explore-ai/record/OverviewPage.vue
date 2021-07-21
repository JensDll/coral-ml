<template>
  <base-title :title="`Models`" @back="$router.back()" back>
    <template #extra>
      <span class="ml-4 text-lg text-gray-600">{{
        $route.params.recordType
      }}</span>
    </template>
  </base-title>
  <base-card-grid class="gap-12">
    <record-card
      v-for="record in records"
      :key="record.id"
      :record="record"
      :on-load-link="onLoadLink"
      @delete="handleDelete"
    ></record-card>
  </base-card-grid>
</template>

<script lang="ts">
import { recordRepository } from '~/api'
import type { Record as ApiRecord } from '~/api'
import RecordCard from './components/RecordCard.vue'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import { defineComponent } from 'vue'

const onLoadLinks: Record<any, string> = {
  '2': 'image-classification',
  '3': 'object-detection'
}

type Data = {
  records: ApiRecord[]
  onLoadLink: string
}

export default defineComponent({
  components: {
    RecordCard,
    BaseTitle,
    BaseCardGrid
  },
  data(): Data {
    return {
      records: [],
      onLoadLink: ''
    }
  },
  async beforeRouteEnter(to, from, next) {
    const { data } = await recordRepository.getWidthRecordTypeId(
      false,
      to.params.recordTypeId as string
    ).promise

    next((vm: any) => {
      vm.records = data?.data
      vm.onLoadLink = onLoadLinks[to.params.recordTypeId as string]
    })
  },
  methods: {
    async handleDelete() {
      const { data } = await recordRepository.getWidthRecordTypeId(
        false,
        this.$route.params.recordTypeId as string
      ).promise
      if (data?.data) {
        this.records = data.data
      }
    }
  }
})
</script>

<style lang="postcss" scoped></style>
