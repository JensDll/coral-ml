<template>
  <div class="mb-4">
    <base-title title="Manage Models" />
  </div>
  <p class="mb-8">
    Learn more about available Models on the
    <base-link href="https://coral.ai/models/">Coral AI Website</base-link>.
  </p>
  <base-card-grid class="gap-12">
    <section
      v-for="{ id, recordType, total, loaded } in recordTypeStore.recordTypes"
      :key="id"
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

<script setup lang="ts">
import { recordTypeRepository } from '~/api'
import { useRecordTypeStore } from '~/store/recordTypeStore'

import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseButton from '~/components/base/BaseButton.vue'
import BaseCardGrid from '~/components/base/BaseCardGrid.vue'
import BaseLink from '~/components/base/BaseLink.vue'
import BaseBadge from '~/components/base/BaseBadge.vue'

const recordTypeStore = useRecordTypeStore()

recordTypeRepository.loadAll().then()
</script>

<style lang="postcss"></style>
