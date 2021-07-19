<template>
  <v-title title="Manage Models">
    <template #text>
      <p>
        Learn more about available Models on the
        <v-link href="https://coral.ai/models/">Coral AI Website</v-link>.
      </p>
    </template>
  </v-title>
  <v-card-grid>
    <section
      v-for="({ id, recordType, total, loaded }, i) in recordTypes"
      :key="i"
    >
      <div class="flex">
        <h3 class="text-xl font-semibold">
          {{ recordType }}
        </h3>
        <v-badge class="ml-4" v-if="loaded">Loaded</v-badge>
      </div>
      <p class="mt-2 mb-4 text-gray-600">
        <span class="mr-2">Available Models</span>
        {{ total }}
      </p>

      <div>
        <v-button
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
        </v-button>
        <v-button
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
        </v-button>
      </div>
    </section>
  </v-card-grid>
</template>

<script lang="ts">
import { recordTypeRepository, recordRepository, Record } from '~/api'
import VTitle from '~/components/base/VTitle.vue'
import VButton from '~/components/base/VButton.vue'
import VCardGrid from '~/components/base/VCardGrid.vue'
import VLoading from '~/components/base/VLoading.vue'
import VLink from '~/components/base/VLink.vue'
import VBadge from '~/components/base/VBadge.vue'

import { defineComponent } from '@vue/runtime-core'
import { RecordType } from '~/api/repositories/recordTypeRepository'

type Data = {
  loadedRecord: Record
  recordTypes: RecordType[]
}

export default defineComponent({
  components: {
    VTitle,
    VButton,
    VCardGrid,
    VLoading,
    VLink,
    VBadge
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
