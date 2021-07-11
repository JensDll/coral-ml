<template>
  <v-page-title title="Manage Models">
    <template #action>
      <v-button
        class="py-2 px-6 rounded font-semibold"
        type="primary"
        @click="$router.push({ name: 'model-new' })"
      >
        Upload New
      </v-button>
    </template>
  </v-page-title>
  <div v-if="state.loading">Loading</div>
  <section class="cards" v-else>
    <model-card
      v-for="model in state.data?.data"
      :key="model.id"
      :model="model"
    ></model-card>
  </section>
</template>

<script setup lang="ts">
import { modelRepository } from '~/api'
import ModelCard from './components/ModelCard.vue'
import VButton from '~/components/base/VButton.vue'
import VPageTitle from '~/components/base/VPageTitle.vue'

const state = modelRepository.getAll(true)
</script>

<style lang="postcss">
.cards {
  display: grid;
  column-gap: 4rem;
  row-gap: 3rem;
  align-items: start;
  grid-template-columns: repeat(auto-fit, minmax(min(20rem, 100%), 1fr));
}
</style>
