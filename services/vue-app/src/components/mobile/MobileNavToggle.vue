<template>
  <div
    v-if="notLandingPage"
    class="
      bg-gray-900
      w-14
      h-14
      rounded-full
      cursor-pointer
      flex
      items-center
      justify-center
      lg:hidden
    "
    @click="navStore.toggleNav()"
  >
    <MenuAlt2Icon class="text-white w-8 h-8" v-if="navStore.navHidden" />
    <XIcon v-else class="text-white w-8 h-8" />
  </div>
</template>

<script setup lang="ts">
import { MenuAlt2Icon } from '@heroicons/vue/solid'
import { XIcon } from '@heroicons/vue/solid'
import { computed } from '@vue/runtime-core'
import { useRouter } from 'vue-router'
import { useNavStore } from '~/store'

const navStore = useNavStore()
const router = useRouter()

const notLandingPage = computed(
  () => router.currentRoute.value.name !== 'landing-page'
)
</script>

<style lang="postcss" scoped></style>
