<template>
  <div class="font-body">
    <LandingPage />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core"
import LandingPage from "./views/LandingPage.vue"

export default defineComponent({
  components: {
    LandingPage
  }
})
</script>

<style lang="postcss">
@import url("https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
</style>
