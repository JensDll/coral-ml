<template>
  <v-title :title="`Models`" @back="router.back()" back>
    <template #extra>
      <span class="ml-4 text-lg text-gray-600">{{
        route.params.recordType
      }}</span>
    </template>
  </v-title>
  <div v-if="state.loading">Loading</div>
  <v-card-grid v-else>
    <model-card
      v-for="model in state.data?.data"
      :key="model.id"
      :model="model"
    ></model-card>
  </v-card-grid>
</template>

<script setup lang="ts">
import ModelCard from './components/VRecordCard.vue'
import VTitle from '~/components/base/VTitle.vue'
import { recordRepository } from '~/api'
import VCardGrid from '~/components/base/VCardGrid.vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const state = recordRepository.getWidthRecordTypeId(
  true,
  route.params.recordTypeId as string
)
</script>

<style lang="postcss" scoped></style>
