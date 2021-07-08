<template>
  <div
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
    v-if="notLandingPage"
  >
    <MenuAlt2Icon
      class="text-white w-8 h-8"
      v-if="store.state.navHidden"
      @click="store.actions.toggleNav()"
    />
    <XIcon
      v-else
      class="text-white w-8 h-8"
      @click="store.actions.toggleNav()"
    />
  </div>
</template>

<script setup lang="ts">
import { MenuAlt2Icon } from "@heroicons/vue/solid"
import { XIcon } from "@heroicons/vue/solid"
import { computed } from "@vue/runtime-core"
import { useRouter } from "vue-router"
import { useStore } from "../../composable"

const store = useStore()
const router = useRouter()

const notLandingPage = computed(() => {
  return router.currentRoute.value.name !== "landing-page"
})
</script>

<style lang="postcss" scoped></style>
