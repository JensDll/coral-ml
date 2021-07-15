<template>
  <v-title :title="`Models`" @back="router.back()" back>
    <template #extra>
      <span class="ml-4 text-lg text-gray-600">{{
        route.params.recordType
      }}</span>
    </template>
  </v-title>
  <v-loading v-if="state.loading">Loading</v-loading>
  <v-card-grid v-else>
    <record-card
      v-for="model in state.data?.data"
      :key="model.id"
      :model="model"
      :on-load-link="onLoadLinks[route.params.recordTypeId]"
      @load="handleLoad"
      @delete="handleDelete"
    ></record-card>
  </v-card-grid>
</template>

<script setup lang="ts">
import RecordCard from '../components/RecordCard.vue'
import VTitle from '~/components/base/VTitle.vue'
import VCardGrid from '~/components/base/VCardGrid.vue'
import VLoading from '~/components/base/VLoading.vue'
import { recordRepository } from '~/api'
import { useRoute, useRouter } from 'vue-router'
import { useSocketService } from '~/composable'
import { computed } from '@vue/runtime-core'

const onLoadLinks: Record<any, string> = {
  '2': 'image-classification',
  '3': 'object-detection'
}

const router = useRouter()
const route = useRoute()

const state = recordRepository.getWidthRecordTypeId(
  true,
  route.params.recordTypeId as string
)

const socketService = useSocketService()

function handleLoad(id: number) {}

async function handleDelete(id: number) {}
</script>

<style lang="postcss" scoped></style>
