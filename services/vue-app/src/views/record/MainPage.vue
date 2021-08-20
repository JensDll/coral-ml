<template>
  <div class="mb-4">
    <base-title title="Manage Models" />
  </div>
  <p class="mb-8">
    Learn more about available Models on the
    <base-link href="https://coral.ai/models/">Coral AI Website</base-link>.
  </p>

  <base-card-grid class="gap-12 items-start">
    <template v-if="loading">
      <base-skeleton v-for="i in 3" :key="i">
        <div class="w-full h-5 skeleton-item"></div>
        <div class="w-3/4 h-5 mt-3 skeleton-item"></div>
        <div class="w-1/2 h-7 mt-8 skeleton-item"></div>
      </base-skeleton>
    </template>
    <template v-else>
      <section
        v-for="{ id, recordType, total, loaded } in recordTypeStore.recordTypes"
        :key="id"
      >
        <div class="flex flex-col items-start lg:flex-row">
          <h3 class="text-xl font-semibold">
            {{ recordType }}
          </h3>
          <base-badge class="mt-2 lg:ml-4 lg:mt-0" v-if="loaded">
            Loaded
          </base-badge>
        </div>
        <p class="mt-2 mb-4 text-gray-600">
          <span class="mr-2">Available Models</span>
          {{ total }}
        </p>
        <div class="flex flex-col items-start lg:flex-row">
          <base-button
            class="py-2 px-6 rounded font-semibold mb-2 lg:mb-0 lg:mr-4"
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
    </template>
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
import BaseSkeleton from '~/components/base/BaseSkeleton.vue'
import { useLoading } from '~/composable'

const recordTypeStore = useRecordTypeStore()

const [[loading, , loadAll]] = useLoading(recordTypeRepository.loadAll)
loadAll().then()
</script>

<style lang="postcss" scoped></style>
