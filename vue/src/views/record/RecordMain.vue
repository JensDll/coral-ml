<template>
  <v-title title="Manage Models">
    <template #text>
      <p>
        Learn more about available Models on the
        <v-link>Coral AI Website</v-link>.
      </p>
    </template>
  </v-title>
  <v-card-grid>
    <section v-for="{ id, recordType, total } in state.data?.data">
      <h3 class="text-xl font-semibold">
        {{ recordType }}
      </h3>
      <p class="mt-2 mb-4 text-gray-600">
        <span class="mr-2">Available Models</span>
        {{ total }}
      </p>
      <div>
        <v-button
          class="py-2 px-6 rounded font-semibold mr-4"
          @click="
            router.push({
              name: 'record-overview',
              params: { recordTypeId: id, recordType }
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

<script setup lang="ts">
import VButton from '~/components/base/VButton.vue'
import VTitle from '~/components/base/VTitle.vue'
import VCardGrid from '~/components/base/VCardGrid.vue'
import VLink from '~/components/base/VLink.vue'
import { recordTypeRepository } from '~/api/repositories/recordTypeRepository'
import { useRouter } from 'vue-router'

const router = useRouter()

const state = recordTypeRepository.getAll(true)
</script>

<style lang="postcss"></style>
