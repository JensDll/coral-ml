<template>
  <base-title title="Manage Models">
    <template #text>
      <p>
        Learn more about available Models on the
        <base-link href="https://coral.ai/models/">Coral AI Website</base-link>.
      </p>
    </template>
  </base-title>
  <base-card-grid class="gap-12">
    <section
      v-for="({ id, recordType, total, loaded }, i) in recordTypes"
      :key="i"
    >
      <div class="flex">
        <h3 class="text-xl font-semibold">
          {{ recordType }}
        </h3>
        <base-badge class="ml-4" v-if="loaded">Loaded</base-badge>
      </div>
      <p class="mt-2 mb-4 text-gray-600">
        <span class="mr-2">Available Models</span>
        {{ total }}
      </p>

      <div>
        <base-button
          class="py-2 px-6 rounded font-semibold mr-4"
          @click="
            $router.push({
              name: 'record-overview',
              params: {
                recordTypeId: id,
                recordType
              }
            })
          "
        >
          View Models
        </base-button>
        <base-button
          class="py-2 px-6 rounded font-semibold"
          type="secondary"
          @click="
            $router.push({
              name: 'record-upload',
              params: { recordTypeId: id, recordType }
            })
          "
        >
          Upload a Model
        </base-button>
      </div>
    </section>
  </base-card-grid>
</template>

<script lang="ts">
import { recordTypeRepository, recordRepository, Record } from '~/api'
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseButton from '~/components/base/BaseButton.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import BaseLoading from '~/components/base/BaseLoading.vue'
import BaseLink from '~/components/base/BaseLink.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'

import { defineComponent } from '@vue/runtime-core'
import { RecordType } from '~/api/repositories/recordTypeRepository'

type Data = {
  loadedRecord: Record
  recordTypes: RecordType[]
}

export default defineComponent({
  components: {
    BaseTitle,
    BaseButton,
    BaseCardGrid,
    BaseLoading,
    BaseLink,
    BaseBadge
  },
  data(): Data {
    return {
      loadedRecord: null!,
      recordTypes: []
    }
  },
  async beforeRouteEnter(to, from, next) {
    const recordType = await recordTypeRepository.getAll(false).promise
    const record = await recordRepository.getLoaded(false).promise
    next((vm: any) => {
      vm.recordTypes = recordType.data?.data
      vm.loadedRecord = record.data
    })
  }
})
</script>

<style lang="postcss"></style>
